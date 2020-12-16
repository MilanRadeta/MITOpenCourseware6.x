#!/usr/bin/env python3

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import math
from PIL import Image
import pathlib
import os

root_folder = pathlib.Path(__file__).parent.absolute().__str__()


def xy_to_index(image, x, y):
    return x * image['width'] + y

def index_to_xy(image, index):
    return index // image['width'], index % image['width'] 

def clip(val, min=0, max=100):
    if val < 0:
        return 0
    
    if val > max:
        return max
    
    return val
    

def get_pixel(image, x, y, use_out_of_bounds=False):
    if use_out_of_bounds:
        x = clip(x, 0, image['height'] - 1)
        y = clip(y, 0, image['width'] - 1)

    index = xy_to_index(image, x, y)
    return image['pixels'][index]


def set_pixel(image, x, y, c):
    index = xy_to_index(image, x, y)
    image['pixels'][index] = c


def apply_per_pixel(image, func):
    result = {
        'height': image['height'],
        'width': image['width'],
        'pixels': image['pixels'].copy(),
    }
    for x in range(image['height']):
        for y in range(image['width']):
            newcolor = func(x, y)
            set_pixel(result, x, y, newcolor)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda x, y: 255-get_pixel(image, x, y))


# HELPER FUNCTIONS

def correlate(image, kernel):
    """
    Compute the result of correlating the given image with the given kernel.

    The output of this function should have the same form as a 6.009 image (a
    dictionary with 'height', 'width', and 'pixels' keys), but its pixel values
    do not necessarily need to be in the range [0,255], nor do they need to be
    integers (they should not be clipped or rounded at all).

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    Kernel should have the same form as a 6.009 image
    """

    assert kernel['height'] % 2 == 1 and kernel['width'] % 2 == 1, 'Kernel must be odd-sized'

    def apply_kernel(x, y):
        result = 0
        for i in range(kernel['height']):
            img_i = x - kernel['height'] // 2 + i
            for j in range(kernel['width']):
                img_j = y - kernel['width'] // 2 + j
                result += get_pixel(kernel, i, j) * get_pixel(image, img_i, img_j, True)
        return result

    return apply_per_pixel(image, apply_kernel)


def round_and_clip_image(image):
    """
    Given a dictionary, ensure that the values in the 'pixels' list are all
    integers in the range [0, 255].

    All values should be converted to integers using Python's `round` function.

    Any locations with values higher than 255 in the input should have value
    255 in the output; and any locations with values lower than 0 in the input
    should have value 0 in the output.
    """
    return apply_per_pixel(image, lambda x, y: round(clip(get_pixel(image, x, y), 0, 255)))

# KERNEL GENERATORS

def gen_empty_kernel(n):
    result = {
        'height': n,
        'width': n,
        'pixels': [0] * n * n,
    }
    return result
    
def gen_box_blur(n):
    result = {
        'height': n,
        'width': n,
        'pixels': [1 / (n * n)] * n * n,
    }
    return result
    
def gen_sharpen(n):
    blur_val = 1 / (n * n)
    result = {
        'height': n,
        'width': n,
        'pixels': [ 2 - blur_val  if i == n // 2 and j == n // 2 else -blur_val  for i in range(n) for j in range(n)]
    }
    return result
    
# FILTERS

def blurred(image, n):
    """
    Return a new image representing the result of applying a box blur (with
    kernel size n) to the given input image.

    This process should not mutate the input image; rather, it should create a
    separate structure to represent the output.
    """
    # first, create a representation for the appropriate n-by-n kernel (you may
    # wish to define another helper function for this)
    blur = gen_box_blur(n)

    # then compute the correlation of the input image with that kernel
    result = correlate(image, blur)

    # and, finally, make sure that the output is a valid image (using the
    # helper function from above) before returning it.
    return round_and_clip_image(result)


def sharpened(image, n):
    return round_and_clip_image(correlate(image, gen_sharpen(n)))


def edges(image):
    hor_sobel = gen_empty_kernel(3)
    ver_sobel = gen_empty_kernel(3)

    hor_sobel['pixels'] = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    ver_sobel['pixels'] = [-1, -2, -1, 0, 0, 0, 1, 2, 1]

    hor_edges = correlate(image, hor_sobel)
    ver_edges = correlate(image, ver_sobel)

    return round_and_clip_image(apply_per_pixel(image, lambda x, y: (get_pixel(hor_edges, x, y) ** 2 + get_pixel(ver_edges, x, y) ** 2)  ** (1 / 2)))

# HELPER FUNCTIONS FOR LOADING AND SAVING GREYSCALE IMAGES

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith('RGB'):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == 'LA':
            pixels = [p[0] for p in img_data]
        elif img.mode == 'L':
            pixels = list(img_data)
        else:
            raise ValueError('Unsupported image mode: %r' % img.mode)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_greyscale_image(image, filename, mode='PNG'):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the 'mode' parameter.
    """
    if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

    out = Image.new(mode='L', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


# HELPERS

def split_color_to_greyscales(image):
    return [{'height': image['height'], 'width': image['width'], 'pixels': list(pixels)} for pixels in zip(*image['pixels'])]

def merge_greyscales_to_color(images):
    return {'height': images[0]['height'], 'width': images[0]['width'], 'pixels': list(zip(*[img['pixels'] for img in images]))}

# VARIOUS FILTERS


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image.
    """
    def color_filter(image):
        channels = split_color_to_greyscales(image)
        filtered = [filt(channel) for channel in channels]
        return merge_greyscales_to_color(filtered)
        
    return color_filter



def make_blur_filter(n):
    return lambda img: blurred(img, n)


def make_sharpen_filter(n):
    return lambda img: sharpened(img, n)


def filter_cascade(filters):
    """
    Given a list of filters (implemented as functions on images), returns a new
    single filter such that applying that filter to an image produces the same
    output as applying each of the individual ones in turn.
    """
    def filter_all(image):
        rem_filters = filters.copy()
        while len(rem_filters) > 0:
            f = rem_filters.pop(0)
            image = f(image)
        return image

    return filter_all


# SEAM CARVING

# Main Seam Carving Implementation

def seam_carving(image, ncols):
    """
    Starting from the given image, use the seam carving technique to remove
    ncols (an integer) columns from the image.
    """
    while ncols > 0:
        ncols -= 1
        grey = greyscale_image_from_color_image(image)
        energy_map = compute_energy(grey)
        cem = cumulative_energy_map(energy_map)
        seam = minimum_energy_seam(cem)
        image = image_without_seam(image, seam)
    return image


def print_image(image):
    for x in range(0, image['height']):
        for y in range(0, image['width']):
            print(get_pixel(image, x, y), end=' ')
        print()
    print()

# Optional Helper Functions for Seam Carving

def greyscale_image_from_color_image(image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image (represented as a dictionary).
    """
    return {'height': image['height'], 'width': image['width'], 'pixels': [round(.299 * pixel[0] + .587 * pixel[1] + .114 * pixel[2]) for pixel in image['pixels']]}


def compute_energy(grey):
    """
    Given a greyscale image, computes a measure of "energy", in our case using
    the edges function from last week.

    Returns a greyscale image (represented as a dictionary).
    """
    return edges(grey)


def cumulative_energy_map(energy):
    """
    Given a measure of energy (e.g., the output of the compute_energy function),
    computes a "cumulative energy map" as described in the lab 2 writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys (but where
    the values in the 'pixels' array may not necessarily be in the range [0,
    255].
    """
    result = {'height': energy['height'], 'width': energy['width'], 'pixels': energy['pixels'].copy()}

    for x in range(1, result['height']):
        for y in range(0, result['width']):
            value = get_pixel(result, x, y)
            value += min([get_pixel(result, x - 1, y + i, use_out_of_bounds=True) for i in range(-1, 2)])
            set_pixel(result, x, y, value)

    return result


def minimum_energy_seam(cem):
    """
    Given a cumulative energy map, returns a list of the indices into the
    'pixels' list that correspond to pixels contained in the minimum-energy
    seam (computed as described in the lab 2 writeup).
    """
    key_fun = lambda k: k[1]
    result = []
    x = cem['height'] - 1
    y, min_val = min([(y, get_pixel(cem, x, y)) for y in range(0, cem['width'])], key=key_fun)
    result.append(xy_to_index(cem, x, y))
    while x > 0:
        x -= 1
        y, min_val = min([(y + j, get_pixel(cem, x, y + j, True)) for j in range(-1, 2)], key=key_fun)
        if y < 0:
            y = 0
        elif y >= cem['width']:
            y = cem['width'] - 1
        result.append(xy_to_index(cem, x, y))

    return result




def image_without_seam(image, seam):
    """
    Given a (color) image and a list of indices to be removed from the image,
    return a new image (without modifying the original) that contains all the
    pixels from the original image except those corresponding to the locations
    in the given list.
    """
    return {'height': image['height'], 'width': image['width'] - 1, 'pixels': [image['pixels'][i] for i in range(len(image['pixels'])) if i not in seam]}


# HELPER FUNCTIONS FOR LOADING AND SAVING COLOR IMAGES

def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, 'rb') as img_handle:
        img = Image.open(img_handle)
        img = img.convert('RGB')  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        w, h = img.size
        return {'height': h, 'width': w, 'pixels': pixels}


def save_color_image(image, filename, mode='PNG'):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
    
    out = Image.new(mode='RGB', size=(image['width'], image['height']))
    out.putdata(image['pixels'])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.

    filter1 = color_filter_from_greyscale_filter(edges)
    filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))

    folder = root_folder + '/test_images'
    outs_and_ops = [
        (root_folder + '/inverted', color_filter_from_greyscale_filter(inverted)),
        (root_folder + '/blurred', color_filter_from_greyscale_filter(make_blur_filter(9))),
        (root_folder + '/sharpened', color_filter_from_greyscale_filter(make_sharpen_filter(7))),
        (root_folder + '/cascade', filter_cascade([filter1, filter1, filter2, filter1])),
    ]
    for img in os.listdir(folder):
        if '.png' in img:
            res = load_color_image('%s/%s' % (folder, img))
            for output, op in outs_and_ops:
                save_color_image(op(res), '%s/%s' % (output, img))

