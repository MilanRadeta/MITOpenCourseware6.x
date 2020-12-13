#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_images(im1, im2):
    assert set(im1.keys()) == {'height', 'width', 'pixels'}, 'Incorrect keys in dictionary'
    assert im1['height'] == im2['height'], 'Heights must match'
    assert im1['width'] == im2['width'], 'Widths must match'
    assert len(im1['pixels']) == im1['height']*im1['width'], 'Incorrect number of pixels'
    assert all(isinstance(i, int) for i in im1['pixels']), 'Pixels must all be integers'
    assert all(0<=i<=255 for i in im1['pixels']), 'Pixels must all be in the range from [0, 255]'
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1['pixels'], im2['pixels'])):
        if i != j:
            pix_incorrect = (ix, abs(i-j))
    assert pix_incorrect == (None, None), 'Pixels must match.  Incorrect value at location %s (differs from expected by %s)' % pix_incorrect



def test_load():
    result = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    compare_images(result, expected)


def test_inverted_1():
    im = lab.load_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    result = lab.inverted(im)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    }
    compare_images(result, expected)

def test_inverted_2():
    input = {
        'height': 1,
        'width': 4,
        'pixels': [15, 75, 156, 193]
    }
    result = lab.inverted(input)
    expected = {
        'height': 1,
        'width': 4,
        'pixels': [240, 180, 99, 62]
    }
    compare_images(result, expected)

@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_inverted_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
    im = lab.load_image(inpfile)
    oim = object_hash(im)
    result = lab.inverted(im)
    expected = lab.load_image(expfile)
    assert object_hash(im) == oim, 'Be careful not to modify the original image!'
    compare_images(result, expected)

def test_correlate_simple():
    image = {
        'height': 5,
        'width': 5,
        'pixels': [35, 40, 41, 45, 50, 40, 40, 42, 46, 52, 42, 46, 50, 55, 55, 48, 52, 56, 58, 60, 56, 60, 65, 70, 75]
    }
    kernel = {
        'height': 5,
        'width': 5,
        'pixels': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    expected = {
        'height': 5,
        'width': 5,
        'pixels': [35, 40, 41, 45, 50, 35, 40, 41, 45, 50, 40, 40, 42, 46, 52, 42, 46, 50, 55, 55, 48, 52, 56, 58, 60]
    }
    result = lab.correlate(image, kernel)
    compare_images(result, expected)

def test_correlate_simple2():
    image = {
        'height': 3,
        'width': 3,
        'pixels': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    }
    kernel = {
        'height': 3,
        'width': 3,
        'pixels': [1, 0, 1, 0, 1, 0, 1, 0, 1]
    }
    expected = {
        'height': 3,
        'width': 3,
        'pixels': [13, 16, 19, 22, 25, 28, 31, 34]
    }
    result = lab.correlate(image, kernel)
    compare_images(result, expected)

def test_round_and_clip():
    image = {
        'height': 3,
        'width': 3,
        'pixels': [-1, 0, 0.25, 0.5, 0.75, 1.1, 254.4, 254.6, 256.1]
    }
    expected = {
        'height': 3,
        'width': 3,
        'pixels': [0., 0., 0., 0., 1, 1, 254, 255, 255]
    }
    result = lab.round_and_clip_image(image)
    compare_images(result, expected)


@pytest.mark.parametrize("kernsize", [1, 3, 7])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_blurred_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.blurred(input_img, kernsize)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)

def test_blurred_black_image():
    image = {
        'height': 5,
        'width': 6,
        'pixels': [0] * 6 * 5
    }
    result = lab.blurred(image, 3)
    compare_images(result, image)
    result = lab.blurred(image, 5)
    compare_images(result, image)

def test_blurred_centered_pixel():
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png')
    image = lab.load_image(inpfile)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                   0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                   0, 0, 0, 0, 28, 28, 28, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    result = lab.blurred(image, 3)
    compare_images(result, expected)

    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0,
                   0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0,
                   0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0,
                   0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                   0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                   0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                   0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                   0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0,
                   0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0,
                   0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0,
                   0, 0, 0,  0,  0,  0,  0,  0, 0, 0, 0],
    }
    result = lab.blurred(image, 5)
    compare_images(result, expected)

@pytest.mark.parametrize("kernsize", [1, 3, 9])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_sharpened_images(kernsize, fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.sharpened(input_img, kernsize)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_edges_images(fname):
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
    input_img = lab.load_image(inpfile)
    input_hash = object_hash(input_img)
    result = lab.edges(input_img)
    expected = lab.load_image(expfile)
    assert object_hash(input_img) == input_hash, "Be careful not to modify the original image!"
    compare_images(result, expected)

def test_edges_centered_pixel():
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png')
    image = lab.load_image(inpfile)
    expected = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0,     0,  0,  0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,  0,  0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,  0,  0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,  0,  0, 0, 0, 0,
                   0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0,
                   0, 0, 0, 0, 255,  0,  255, 0, 0, 0, 0,
                   0, 0, 0, 0, 255, 255, 255, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,   0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,   0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,   0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,     0,   0, 0, 0, 0, 0],
    }
    result = lab.edges(image)
    compare_images(result, expected)

if __name__ == '__main__':
    import sys
    import json

    class TestData:
        def __init__(self):
            self.results = {'passed': []}

        @pytest.hookimpl(hookwrapper=True)
        def pytest_runtestloop(self, session):
            yield

        def pytest_runtest_logreport(self, report):
            if report.when != 'call':
                return
            self.results.setdefault(report.outcome, []).append(report.head_line)

        def pytest_collection_finish(self, session):
            self.results['total'] = [i.name for i in session.items]

        def pytest_unconfigure(self, config):
            print(json.dumps(self.results))

    if os.environ.get('CATSOOP'):
        args = ['--color=yes', '-v', __file__]
        if len(sys.argv) > 1:
            args = ['-k', sys.argv[1], *args]
        kwargs = {'plugins': [TestData()]}
    else:
        args = ['-v', __file__] if len(sys.argv) == 1 else ['-v', *('%s::%s' % (__file__, i) for i in sys.argv[1:])]
        kwargs = {}
    res = pytest.main(args, **kwargs)
