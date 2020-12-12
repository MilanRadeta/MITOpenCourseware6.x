# Pose-controlled Spotify Playback!
### Tutorial by Julie Ganeshan (edited by Adam Chlipala [with code by Adam Hartz] to connect to CAT-SOOP instead of Spotify)

### Originally Written for MIT 6.009's Last Recitation (Fall 2020)

## Idea
What if, during the 1 hour of recitation, you could control your music playback using just your hand!
This is split into 4 parts.

(a) Setup - install various libraries and clone some repos
(b) Basic Gesture Recognition, for left and right swipes
(c) Local playback control, via macros
(d) Web playback control, via Spotify's Web API


Additionally, the instructor will have to set-up a spotify session so that all the students can connect to it.

# Part 1: Setup
I've created a new python 3.8 environment in Anaconda on Windows. I'll assume `python` and `pip` are correctly defined in PATH,
and that students can use the terminal. (You can always use `python -m pip` to access pip, too)

## Install Pytorch
PyTorch is a deep learning library, which we'll be using to run our pose-detector. 
The most up-to-date install info, and GPU instructions, can be found here:
https://pytorch.org/get-started/locally/

Since we don't need it to be super-fast-running, we can just use the CPU pip version. At the time of writing,
this can be downloaded via:

Windows:
```
pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
```

Mac:
```
pip install torch torchvision torchaudio
```

Linux:
```
pip install torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
```

## Install OpenCV
OpenCV is a computer vision library. We'll only be using it to access the webcam.

You can install it with
```
pip install opencv-python
```

## Install Requests
Requests is a networking library that lets you easily write HTTP requests in Python. (GET/POST/etc)
It's super popular, easy to use, and very flexible.

```
pip install requests
```

## Install PyAutoGUI
We'll use PyAutoGUI to create macros that let us use our computer with pose. It's cross platform, and
is also on pip!

```
pip install pyautogui
```

## Install TQDM
TQDM is a lightweight progress-bar library. The code we'll download uses it

```
pip install tqdm
```

## [Optional] Install spotipy
Spotipy is a python library that sends spotify requests in a nice way. We'll do most of our
requests manually, to get practice with HTTP requests, but Spotipy handles authorization
nicely, so, if you want to control *your* music (required for instructors), you'll need this
to handle the authorization flow.

```
pip install spotipy
```

## Download the PoseNet Pytorch port
PoseNet is Google's lightweight 2D pose network. It's been ported to PyTorch. We'll
use my favorite pose repo for this tutorial (found at https://github.com/rwightman/posenet-pytorch):

```
git clone https://github.com/rwightman/posenet-pytorch.git
```

# Part 2: Pose Detection and Gesture Recognition

## Step 1. Change Execution Device
Unfortunately, the demo, as written, assumes a GPU is being used. Let's change this!

Open up `webcam_demo.py` with your favorite text editor. Then, ctrl+f for the search term `cuda` (the name of the GPU device, in Python). You should find 2 occurrences.

One on line 19, that tells the entire model to run on the GPU,
```python
model = model.cuda() # Line 19
```

And one on line 33, that tells the input to the model to be put on the GPU.
```python
input_image = torch.Tensor(input_image).cuda() # Line 33
```

We want it to run on the CPU! So let's replace those `cuda()` calls with `cpu()` calls.

```python 
model = model.cpu() # Line 19, Used to be .cuda()
input_image = torch.Tensor(input_image).cpu() # Line 33, Used to be .cuda()
```

## Step 2. Run Pose Detector

Now, it should run on the cpu! Since we're the CPU isn't as fast as a GPU, to run our model, we'll make the input really small (read frames at 640x480 pixels,
and halve the size before analyzing it)

If you want to use a different webcam, you can change `cam_id`, to another number for a different connected webcam, or even a video file name.

This will take a bit to launch the first time, as it has to download the model
weights from the internet. This uses requests, which we'll learn how to use soon!
```
cd posenet-pytorch
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

Take a step back, and you should see dots and lines drawn where the computer sees you! Press Q to quit.

**Tip**: For technical reasons, only one application can access your webcam at a time. So, if your python program can't read your webcam, make sure that you're not using it for another application! (Like Jitsi Meet, Zoom, etc)

If everything has been installed, you have a webcam, and you've correctly changed GPU -> CPU, you should have something that look like this! 

[http://prntscr.com/vpe3us](http://prntscr.com/vpe3us)

Try waving at the camera! It will be a little noisy, possibly a little slow, and results may vary depending on your lighting / clothes etc. It'll work better when it can see most of your body. But - it works!


## Step 3. Intercept Poses

This demo looks cool! But we want to actually use the poses to do something!
So, now we'll modify the code so that it creates an instance of a class,
and calls a function whenever it gets a pose!

We don't need to understand exactly how everything works, but we *do* know that
the program, at some point, needs to draw everything! So, let's look for where
the program draws to the screen - it should have all our keypoints, then.

Here's a breakdown of what's happening, based on the looping structure, and some
deductions on variable names

[http://prntscr.com/vpea42](http://prntscr.com/vpea42)

Importantly, it looks like we should do any setup before the `while` loop, and during the while loop, we can access the 
score & positions of each of the tracked keypoints via the variables `keypoint_scores` and `keypoint_coords`. Can you imagine
how much harder this would have been were they named `x` and `y`? Readable code is important so that people can extend your code!


Let's start off by making a class `GestureControlledObject`. It can store arbitrary state, and will have an `on_pose_frame` function
that takes in the scores and coordinates of the keypoints which will be called every time we get a frame.

```python
# Above main, line 16
class GestureControlledObject:
    def __init__(self):
        pass
    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        pass
```

Now, let's make an instance of this class, before the while loop!

```python 
# Existing before
model = posenet.load_model(args.model)
model = model.cpu()
output_stride = model.output_stride

# Add it with the other assorted setup
gesture_controlled_object =  GestureControlledObject()

# Existing after
cap = cv2.VideoCapture(args.cam_id)
```

And, let's call it every frame, by putting it in the while loop, just before
we show the drawn version!
```python
# Existing before
overlay_image = posenet.draw_skel_and_kp(
            display_image, pose_scores, keypoint_scores, keypoint_coords,
            min_pose_score=0.15, min_part_score=0.1)

# Call our interceptor!
gesture_controlled_object.on_pose_frame(keypoint_scores, keypoint_coords)

# Existing after
cv2.imshow('posenet', overlay_image)
```

Finally, let's add a basic implementation of `on_pose_frame`, that just tells
us the type of each of the inputs! After all - we don't exactly know WHAT we're
gonna be passed!

```python
class GestureControlledObject:
    def __init__(self):
        pass
    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        # Let's just print the types, for now
        print(f"Score type: {type(keypoint_scores)}. Coord type: {type(keypoint_coords)}")
```

This will *definitely* slow it down, because it'll print to the screen (which is actually really slow).
But that's okay, we won't be using this for long.

Let's try running again!
```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

You should see this, repeated a bunch of times.
```
Score type: <class 'numpy.ndarray'>. Coord type: <class 'numpy.ndarray'>
```

So, it looks like we're getting `ndarray` objects, which are defined in numpy!
...
What are those? Let's launch a python REPL, and use `help` to find out more.

```
Python 3.8.5 (default, Sep  3 2020, 21:29:08) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy
>>> help(numpy.ndarray)
Help on class ndarray in module numpy:

class ndarray(builtins.object)
 |  ndarray(shape, dtype=float, buffer=None, offset=0,
 |          strides=None, order=None)
 |
 |  An array object represents a multidimensional, homogeneous array
 |  of fixed-size items.  An associated data-type object describes the
 |  format of each element in the array (its byte-order, how many bytes it
 |  occupies in memory, whether it is an integer, a floating point number,
 |  or something else, etc.)
...
>>> exit()
```

Okay! So, they're multi-dimensional arrays. They have some attribute `shape`, that defines
what shape the whole array is.

This is similar to the ND arrays we used in Six-Double-Oh-Mines, *but* it's actually all stored
internally as 1 array, like the image labs at the begnning of term!

Fortunately, ND arrays have a handful of useful features for us (you can find this by googling "numpy")

1. They implement the dunders `__getitem__` and `__setitem__`! You can access a particular element using comma-seperated indices. You can also use just one index at a time, and access them like nested-lists.
2. They have an attribute `shape` that is a tuple with the full n-dimensional shape.

Let's change our print statements to tell us what the shapes of each of these arrays are!

```python
class GestureControlledObject:
    def __init__(self):
        pass
    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        # Let's just print the types, for now
        # print(f"Score type: {type(keypoint_scores)}. Coord type: {type(keypoint_coords)}")
        print(f"Score shape: {keypoint_scores.shape}. Coord type: {keypoint_coords.shape}")
```

Now, run again!
```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```
Now it'll print something like:
```
Score shape: (10, 17). Coord type: (10, 17, 2)
```

Okay! So we're getting some N-dimensional arrays every frame! Let's move onto the next step!

## Step 4. Getting one keypoint
We know that each frame, we're getting a score array, and a coordinate array. But what do these mean?

We have arrays of shape:
```
Score shape: (10, 17). Coord type: (10, 17, 2)
```

Each of these starts with (10, 17). This means there are 10 "rows", and 17 "columns" for each.
The score is 1 number, and the coordinate is a list of 2 numbers (thus adding a dimension).

To understand exactly what this means, we'll have to look at what PoseNet is supposed to do - it promises
the (x,y) coordinates of 17 different keypoints (neck, wrist, elbows, and so forth) for up to 10 people in a given image. It also promises a score, between 0 and 1, for how certain it is that that keypoint is really detected. Scores of 0 means the model doesn't have any certainty, and 1 means a human keypoint is definitely there.

That explains our shape!

Our score is 10 x 17 -- 10 people, 17 keypoints, 1 score per.
Our coordinates are 10 x 17 x 2 -- 10 people, 17 keypoints, 2 coordinates (x and y) for each!

For our use-case, we'll only want to track one person. We'll arbitrarily choose the FIRST person in each
frame.

```
class GestureControlledObject:
    def __init__(self):
        pass
    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        first_person_scores = keypoint_scores[0]
        first_person_coords = keypoint_coords[0]
```

Now, we have a length 17 array of scores per keypoint, and a 17 x 2 array with the x/y coordinate of each keypoint.

Now, let's just track one keypoint, by indexing into this array.. We'll use the right-wrist. The library we're using
actually provides a handy dictionary, `PART_IDS` too lookup a part by name! You can see the codebehind
in `posenet/constants.py`

Finally, let's just print the wrist's position and score!

Your gesture controller should now look like this. I've added in the .2f specifier
so that my decimals print with 2 digits after the decimal point.

```python
class GestureControlledObject:
    def __init__(self):
        pass
    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        # Get just the first detected person
        first_person_scores = keypoint_scores[0]
        first_person_coords = keypoint_coords[0]

        # from posenet/constants.py
        RIGHT_WRIST_ID = posenet.PART_IDS['rightWrist']
        
        # Now, lookup this keypoint
        # A number (0..1)
        wrist_score = first_person_scores[RIGHT_WRIST_ID]
        # A list (x,y), from (0..width, 0..height). We've chosen
        # width = 640 and height = 480, in command line args
        wrist_coord = first_person_coords[RIGHT_WRIST_ID]
        # Break this into x, y coordinates
        wrist_x, wrist_y = wrist_coord

        print(f"Wrist @ ({wrist_x:.2f}, {wrist_y:.2f}). Certainty: {wrist_score:.2f}")
```

Running again.
```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

The positions are specified with respect to the TOP-LEFT of the frame, with X
going from 0 to the width of the frame (640) and y going from 0 to the height (480)

Try moving your hand, and seeing how X, Y and score, change accordingly!
Now, we can track a user's wrist! Let's start using it!

## Step 5. Using the wrist position for gesture recognition

Now, let's make a gesture recognizer! First, let's make a function that takes in 
the wrist position and score, handles it! Our `on_pose_frame` has already gotten pretty big

```python
class GestureControlledObject:
    def __init__(self):
        pass

    def analyze_wrist_position(self, wrist_score, wrist_x, wrist_y):
        pass

    def on_pose_frame(self, keypoint_scores, keypoint_coords):
        # EXTRACTION CODE
        ...
        ...

        # Call a function, INSTEAD of printing!

        # Was:
        # print(f"Wrist @ ({wrist_x:.2f}, {wrist_y:.2f}). Certainty: {wrist_score:.2f}")
        # Now:
        self.analyze_wrist_position(wrist_score, wrist_x, wrist_y)
```

The first thing we'll need to do is toss out any frame where the score is too 
low - that means our detection failed! We'll just arbitrarily choose a threshold
of 0.5. If the score is higher than this value, we'll accept that the wrist is at the given
location. More sophisticated models could actually use this number, but let's keep it simple.

```python
class GestureControlledObject:
    def __init__(self):
        pass

    def analyze_wrist_position(self, wrist_score, wrist_x, wrist_y):
        if wrist_score < 0.5:
            # Bad reading. Ignore
            return
        else:
            # Good reading! Let's do stuff!
            pass
```

Now, let's make our gesture detector, to find out when the user has swiped
left or right! We'll use a really simple gesture detector but you could try
making something better!

Our gesture detector will keep track of the last 30 frames (about 1-2 seconds).
If the wrist's x position has moved more than some number of pixels in that time,
we'll treat it as a swipe!

This means we'll need some state, that'll persist through multiple `analyze_wrist_position` calls
(multiple frames). Let's put it in `__init__`. We'll also add some arbitrary configuration constants
to use for detection.

```python
class GestureControlledObject:
    def __init__(self):
        self.n_frames_to_store = 30
        self.swipe_threshold = 100
        self.prev_frame_x_values = []
```

Now, let's implement the rest of `analyze_wrist_position`! We'll need to first add 
the wrist position to our position history (`prev_frame_x_values`), clearing old data as needed.
Then, we can tell if it's a swipe by looking at how far the two farthest X values are.
Finally, by seeing which came first (the left or right endpoint), we can see if it's a swipe left or 
a swipe right.

It should look something like this, after:

```python
def analyze_wrist_position(self, wrist_score, wrist_x, wrist_y):
        if wrist_score < 0.5:
            # Bad reading. Ignore
            return
        else:
            # Good reading! Let's do stuff!
            self.prev_frame_x_values.append(wrist_x)
            # Do we have too many frames stored?
            n_frames_extra = len(self.prev_frame_x_values) - self.n_frames_to_store
            if n_frames_extra > 0:
                # Yes. Trim off extra from beginning (oldest)
                self.prev_frame_x_values = self.prev_frame_x_values[n_frames_extra:]
            
            # Check if we've traversed enough x
            rightmost_x = max(self.prev_frame_x_values)
            leftmost_x = min(self.prev_frame_x_values)
            if abs(rightmost_x - leftmost_x) > self.swipe_threshold:
                # We've gone pretty far! This is a swipe!
                # Was it left or right?
                rightmost_index = self.prev_frame_x_values.index(rightmost_x)
                leftmost_index = self.prev_frame_x_values.index(leftmost_x)
                # Now that we know, clear the history. This way we have to move
                # again to get another swipe.
                self.prev_frame_x_values.clear()
                if rightmost_index > leftmost_index:
                    # We went left->right in the image, so right->left irl.
                    # A left swipe!
                    self.on_swipe_left()
                elif leftmost_index > rightmost_index:
                    # We went right->left in the image, so left->right irl.
                    # A right swipe!
                    self.on_swipe_right()
```

This is getting big again! So, we added in function calls to `self.on_swipe_left()`
and `self.on_swipe_right()`. Let's define those. Note that we're calling
`on_swipe_left` when we go FROM left TO right. This is because our webcam mirrors us!
(So moving right in the image = moving left in the real world)

```
class GestureControlledObject:
    def __init__(self):
        self.n_frames_to_store = 30
        self.swipe_threshold = 100
        self.prev_frame_x_values = []

    def on_swipe_left(self):
        print("SWIPE LEFT")
    
    def on_swipe_right(self):
        print("SWIPE RIGHT")
```

Finally, let's test this! It should now print "SWIPE LEFT" and "SWIPE RIGHT"
as it sees you move!

```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

Try changing the parameters of the swipe to suit your setup
a bit more. By storing more frames, you can move your hand more slowly. By reducing
the swipe threshold, you can reduce the distance needed to travel to swipe. I found
values of 20 frames, and 40 pixels worked well when sitting at my desk.

## Conclusion
Great work! Now, we've modified an existing code-base to run our code as it
gets poses. We did a little bit of reverse engineering to find out how this
data is formatted, and finally, we used the wrist's pose to create a simple 
left/right swipe detector. In the next parts, we'll see some fun things we can
do with the detected gesture!

# Part 2.999: Sending Emoji Requests to CAT-SOOP

Here we interrupt Julie's original flow to do something simpler:
use your gestures to trigger emoji reactions in this very recitation.

Here's a function definition for sending a reaction to our server.

```
import requests

URL = 'https://py.mit.edu/rec/emote'
TOKEN = "FILL THIS IN"

def catsoop_emote(i):
    print('Emoji:', i)
    x = requests.post(URL, data = {'api_token': TOKEN, 'icon': i})
    return x.json()
```

Replace the `TOKEN` definition with the long string you see on the recitation web page.
Every browser tab with that page open gets a unique token,
which our server can use to tell which user is requesting the reaction.

We use the nifty `requests` library for interacting with the server.
A `POST` is a kind of web request that asks for the server to take some action.
Those requests may take all kinds of data; we extended CAT-SOOP to expect the two
fields `api_token` and `icon` given here.
A call to `requests.post` returns the server's response to the request.
For this example, that response just indicates success vs. failure.
(Actually, the HTTP protocol behind the web has a more idiomatic way to indicate
success vs. failure with *status codes*, but we have simplified here.)

Now it should be easy to replace your swipe responses with calls to this function.

OK, back to Julie's example with controlling Spotify.

# Part 3: Local Playback Control with Gestures

Now that we can recognize when a user's swiping left and right, let's use that to
affect what song is playing, on the local machine! To do this, we'll send 
the "next song" and "previous song" keystrokes that are on some media keyboards,
that all computers / operating systems have responses too. What exactly will happen will vary depending
on your music player and operating system.

## Step 1: Make playback functions separately

We don't want to think about pose control yet, so let's just implement a `next_song` and `previous_song`
function in our python script.

Let's start off by importing `pyautogui`, a library that can send keystrokes to your computer!
We'll also turn on failsafe mode. Just to be safe! You can disable this, if you want to 
be able to use your mouse in the topleft corner of the screen (test your code first, though!)

```python
# Somewhere near the top
import pyautogui
# Enable the "Failsafe" mode that throws an error when your mouse
# moves to the topleft corner. In case something goes wrong, you might
# not be able to use your keyboard normally to stop the program.
pyautogui.FAILSAFE = True
```

Now, let's use it to send keystrokes!
```python
# Somewhere in the outermost code, similar to main()

'''
Sends the next song & previous song keystrokes
You can see all available keys in:
pyautogui.KEYBOARD_KEYS
The one's we're interested in are: ['nexttrack', 'prevtrack']
'''
def next_song_local():
    pyautogui.press('nexttrack')

def previous_song_local():
    pyautogui.press('prevtrack')
```

## Step 2: Call playback functions on swipe
Now, let's call our playback functions! Back into the `GestureControlledObject`
class...

```python
def on_swipe_left(self):
    print("SWIPE LEFT")
    previous_song_local()
    
def on_swipe_right(self):
    print("SWIPE RIGHT")
    next_song_local()
```

## Step 3: Test it!
Now, go ahead and play some music! Make sure it's a music player that's
well integrated into your system (like Spotify, RhythmBox on Ubuntu, 
Groove on Windows, iTunes on Mac, Youtube in Chrome on some machines)

Run your pose-detector, and try changing songs!

```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

You can use `pyautogui` for a bunch of other stuff too! You can send clicks,
move the mouse according to your wrist position, and more!

## Step 4: Rate Limiting
Now that we're skipping songs, we don't usually want to skip many times a second.
Let's add a rate limit check so that swiping only does something
once every few seconds. We'll use the `time.time()` function to get a decimal
representing the current time, in seconds since 1970. That means we 
can subtract two such times to get the number of seconds elapsed!

```python
def __init__(self):
        self.n_frames_to_store = 20
        self.swipe_threshold = 40
        self.prev_frame_x_values = []
        
        # Absolute time of last swipe
        self.last_swipe_time = 0
        # Don't allow more than 1 swipe per 3 seconds
        self.min_seconds_between_swipes = 3

    def rate_limit_check(self):
        # Check difference between now & previous swipe
        current_time = time.time()
        time_since_last_swipe = current_time - self.last_swipe_time
        # Was this too soon?
        allowed = time_since_last_swipe > self.min_seconds_between_swipes
        if allowed:
            # We're allowing a swipe, so update previous swipe time
            self.last_swipe_time = current_time
        # Return if we're allowed
        return allowed

    def on_swipe_left(self):
        if self.rate_limit_check():
            print("SWIPE LEFT")
            previous_song_local()
        else:
            print("Rejected swipe left")
    
    def on_swipe_right(self):
        if self.rate_limit_check():
            print("SWIPE RIGHT")
            next_song_local()
        else:
            print("Rejected swipe right")
```

As always, run to test! Now it shouldn't let you skip songs too frequently
```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

## Step 5: Queue Clearing
You might have noticed that when it can't see our hand for a long time,
then it starts seeing it, it might register a swipe! This is because we only
store frames when it's valid hand data! Let's clear out data when we get invalid
hand data!

```python
def analyze_wrist_position(self, wrist_score, wrist_x, wrist_y):
        if wrist_score < 0.5:
            # Bad reading. Clear oldest frame
            if len(self.prev_frame_x_values) > 0:
                self.prev_frame_x_values.pop(0)
            return
```

Test again! Now it should be a little more robust.
```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```

## Conclusion
Now we can skip songs forward and backward! By building it out using functions,
we hardly had to think about pose (just about what happens when you swipe) to 
get our playback controls working!

# Part 4: Spotify Playback
So far, we've managed to get a playback controller for our local machine, which
we can control with our pose. What if we wanted to control something else,
on the web? We can use a web API (**A**pplicatation **P**rogamming **I**nterface) for this!

We'll be demonstrating using Spotify's API, which is pretty well documented, ties
nicely with our pose-playback controller, and has its own web servers.
However, the techniques we use are universal across most web APIs!

Note that the playback functions we're using only work with Spotify Premium...

## Requests - GET / POST and their siblings

Before we get started - how does web programming even work? Note that here, we're
interested in *web services* - that is, bits of code that are exposed via the web,
that allow you to call them without ever downloading the code to your machine. This isn't
to be confused with *web sites* which are marked-up text documents that a user sees.

Many popular services (youtube, google search, spotify, reddit, to name a few) offer 
*developer-facing* API's that let you call their various services. 

Every web API has a URL - a string that specifies where to find it on the web.
Spotify's lives here:

[https://api.spotify.com/](https://api.spotify.com/)

You can access various functions by using different URL's. The URL's of the various
services will vary per API.

Once you have a URL, it's like having a name to a python function.
However, when requesting data from a web service, you also need to provide a *verb* 
describing what you'd like to do.

The two used most often are:

- **GET** (read data from a website, at the given URL. This is 
what your web browser does when you type something in the address bar).
- **POST** (read AND write data to a website, with the given URL)

GET's are like calling a function. POST's are like calling a function, but with arguments.

All the spotify APIs need some data from you (namely, an authorization token). 

Here's a pokemon API that only needs a GET request though!
[https://pokeapi.co/api/v2/pokemon/ditto](https://pokeapi.co/api/v2/pokemon/ditto)

Unfortunately, when you send data to a website, you need some way to encode it!
One standard format is called `JSON`. It basically lets you write python dictionaries, lists, numbers, strings, and booleans. It's written just like it is in python.

We'll use the `requests` library, which handles all the networking code-behind, and let's
us GET and POST requests. It also provides handy functions to convert to-and-from JSON via python dictionaries.

Here's the python code that GETs ditto's information, as a python dictionary, and prints
the keys given to us. It's really extensive...

```python
import requests
ditto_info = requests.get("https://pokeapi.co/api/v2/pokemon/ditto").json()
print(ditto_info.keys())
```

## [Optional, Required for instructors] Step 1. Setup Spotify Authentication

Since APIs are powered by real servers, somewhere, you often can't use them freely.
Many APIs require you to register your app, and authenticate, so that they can make sure
you're not overloading their servers.

Normally, you'd need to register an app here:
[https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications)

Once you have, you'll get a "client secret" and a "client ID" - the username and password for your spotify app. Then you'd authenticate the user, who's using your app.

BUT, we'll simplify things by using the Spotify test API.

Go here:
[https://developer.spotify.com/console/post-next/](https://developer.spotify.com/console/post-next/)

And click the "Get Token" button, with the scope "user-modify-playback-state"
This will put a long token, that's valid for 24 hours into the OAuth token box.

Share this token with your students!

## Step 2. Use the token to control Spotify

Since we now have an authentication key (ask instructor, if you want to control
the recitation's player), we can call various aspects of the Spotify API!

According to the API documentation here:

[Next Track](https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-next-track/)

[Previous Track](https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-previous-track/)

We can POST to these urls to skip forward / backward in playback:
```
https://api.spotify.com/v1/me/player/next
https://api.spotify.com/v1/me/player/previous
```

Additionally, we need to specify "headers" which is key-value pairs for data.
This is similar to the content of a request, but headers are usually used for things
like usernames / passwords, while the "content" is used for data that pertains 
to that particular request.

The header should be set up like (based on spotify doc):
```python
SPOTIFY_AUTH_TOKEN = "PASTE_CODE_HERE"
AUTH_HEADER = {
    "Authorization": f"Bearer {SPOTIFY_AUTH_TOKEN}"
}
```

Let's make functions to call this! We'll print whatever is returned raw, as we don't really care about it.
(We have to use decode() to turn it into letters)
```python
# Somewhere near the top
import requests

# Somewhere near your next_song functions
def next_song_spotify():
    response = requests.post("https://api.spotify.com/v1/me/player/next", headers=AUTH_HEADER)
    print(f'Response: "{response.content.decode()}"')

def previous_song_spotify():
    response = requests.post("https://api.spotify.com/v1/me/player/previous", headers=AUTH_HEADER)
    print(f'Response: "{response.content.decode()}"')
```

Finally, let's tie this to our gesture recognizer!

```python
def on_swipe_left(self):
    if self.rate_limit_check():
        print("SWIPE LEFT")
        previous_song_spotify() # Now spotify, instead of local
    else:
        print("Rejected swipe left")

def on_swipe_right(self):
    if self.rate_limit_check():
        print("SWIPE RIGHT")
        next_song_spotify() # Now spotify, instead of local
    else:
        print("Rejected swipe right")
```

All that's left to do is test!

## Step 3. Control Spotify!
Run as usual.

```bash
python webcam_demo.py --cam_id 0 --cam_width 640 --cam_height 480 --scale_factor 0.5
```











