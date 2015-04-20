__author__ = 'tjs'

import unittest

import numpy as np

from main.cgr import find_word_coords, cgr_distance


class WordCoordinateTest(unittest.TestCase):

    def test_word_length_1(self):
        self.assertEqual(find_word_coords('C'), (0, 0))
        self.assertEqual(find_word_coords('G'), (1, 0))
        self.assertEqual(find_word_coords('A'), (0, 1))
        self.assertEqual(find_word_coords('T'), (1, 1))
        
    def test_word_length_2(self):
        self.assertEqual(find_word_coords('CC'), (0, 0))
        self.assertEqual(find_word_coords('GC'), (1, 0))
        self.assertEqual(find_word_coords('AC'), (0, 1))
        self.assertEqual(find_word_coords('TC'), (1, 1))
        
        self.assertEqual(find_word_coords('CG'), (2, 0))
        self.assertEqual(find_word_coords('GG'), (3, 0))
        self.assertEqual(find_word_coords('AG'), (2, 1))
        self.assertEqual(find_word_coords('TG'), (3, 1))
        
        self.assertEqual(find_word_coords('CA'), (0, 2))
        self.assertEqual(find_word_coords('GA'), (1, 2))
        self.assertEqual(find_word_coords('AA'), (0, 3))
        self.assertEqual(find_word_coords('TA'), (1, 3))
        
        self.assertEqual(find_word_coords('CT'), (2, 2))
        self.assertEqual(find_word_coords('GT'), (3, 2))
        self.assertEqual(find_word_coords('AT'), (2, 3))
        self.assertEqual(find_word_coords('TT'), (3, 3))

    def test_adjacent_words(self):
        # Words that differ in just 1 letter are always adjacent
        # TODO: generate words from length 3-8 and ensure this
        self.skipTest("Not Implemented")


class WordsFromSequenceTest(unittest.TestCase):
    pass  # TODO: WordsFromSequenceTest


class CreateCgrTest(unittest.TestCase):
    pass  # TODO: CreateCgrTest


class CgrDistanceTest(unittest.TestCase):

    def test_zero_cgr(self):
        a = np.ones((4, 4))
        b = np.zeros((4, 4))

        # a contains 16 values 1, so the distance is the square root of 16
        self.assertEqual(cgr_distance(a, b), 4)
        self.assertEqual(cgr_distance(a, b), cgr_distance(b, a))

    def test_equal_cgr(self):
        a = np.ones((4, 4))
        b = np.ones((4, 4))

        self.assertEqual(cgr_distance(a, b), 0)
        self.assertEqual(cgr_distance(a, b), cgr_distance(b, a))

    def test_incompatible_cgr(self):
        a = np.random.random((4, 4))
        b = np.random.random((2, 2))

        with self.assertRaises(ValueError):
            cgr_distance(a, b)