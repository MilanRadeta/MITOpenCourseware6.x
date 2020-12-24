#!/usr/bin/env python3
import os
import ast
import mixtape
import types
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


class TestMixtape(unittest.TestCase):
    def _test_from_file(self, n):
        with open(os.path.join(TEST_DIRECTORY, 'test_outputs', 'songs_%02d.py' % n), 'r') as f:
            (songs, target, valid) = ast.literal_eval(f.read())
        result = mixtape.mixtape(dict(songs), target)
        if valid:
            self.assertNotEqual(result, None)
            self._test_valid(songs, target, result)
        else:
            self.assertEqual(result, None)

    def _test_valid(self, songs, target, result):
        self.assertEqual(len(result), len(set(result)))
        self.assertTrue(all(s in songs for s in result))
        self.assertEqual(sum(songs[i] for i in result), target)

    def test_00_examples(self):
        songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
        self._test_valid(songs, 11, mixtape.mixtape(dict(songs), 11))
        self.assertEqual(mixtape.mixtape(dict(songs), 1000), None)
        self._test_valid(songs, 21, mixtape.mixtape(dict(songs), 21))

    def test_01(self):
        for i in range(1, 6):
            self._test_from_file(i)

    def test_02(self):
        for i in range(6, 11):
            self._test_from_file(i)

    def test_03(self):
        for i in range(11, 16):
            self._test_from_file(i)

    def test_04(self):
        for i in range(16, 21):
            self._test_from_file(i)

    def test_05(self):
        for i in range(21, 26):
            self._test_from_file(i)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
