#!/usr/bin/env python3

import math

from PIL import Image as Image
import pathlib
import os

root_folder = pathlib.Path(__file__).parent.absolute().__str__()

# NO ADDITIONAL IMPORTS ALLOWED!

def xy_to_index(image, x, y):
    return x * image['width'] + y

def clip(val, min=0, max=100):
    if val < 0:
        return 0
    
    if val > max:
        return max
    
    return val
    

def get_pixel(image, x, y, use_out_of_bounds=False):
    if use_out_of_bounds:
        x = clip(x, 0, image['height'] - 1)
        y = clip(x, 0, image['width'] - 1)

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
            for j in range(kernel['width']):
                kernel_index = xy_to_index(kernel, i, j)
                img_i = clip(x - kernel['height'] // 2 + i, 0, image['height'] - 1)
                img_j = clip(y - kernel['width'] // 2 + j, 0, image['width'] - 1)
                img_index = xy_to_index(image, img_i, img_j)
                result += kernel['pixels'][kernel_index] * image['pixels'][img_index]
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


# FILTERS

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



# HELPER FUNCTIONS FOR LOADING AND SAVING IMAGES

def load_image(filename):
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


def save_image(image, filename, mode='PNG'):
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

    
if __name__ == '__main__':
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    folder = root_folder + '/test_images'

    identity = gen_empty_kernel(3)
    identity['pixels'][4] = 1

    translation = gen_empty_kernel(5)
    translation['pixels'][10] = 1

    average = {
        'height': 3,
        'width': 3,
        'pixels': [0, 0.2, 0, 0.2, 0.2, 0.2, 0, 0.2, 0]
    }

    tran_down_right = gen_empty_kernel(9)
    tran_down_right['pixels'][18] = 1

    outs_and_ops = [
        (root_folder + '/inverted', inverted),
        (root_folder + '/identity', lambda image: correlate(image, identity)),
        (root_folder + '/translation', lambda image: correlate(image, translation)),
        (root_folder + '/average', lambda image: round_and_clip_image(correlate(image, average))),
        (root_folder + '/tran_down_right', lambda image: round_and_clip_image(correlate(image, tran_down_right))),
        (root_folder + '/blurred', lambda image: blurred(image, 5)),
    ]
    for img in os.listdir(folder):
        if '.png' in img:
            res = load_image('%s/%s' % (folder, img))
            for output, op in outs_and_ops:
                save_image(op(res), '%s/%s' % (output, img))
