from __future__ import division

from collections import Counter

import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


# Translation from Amino Acids to DNA, as described in Section 2.2
AA_DNA_TRANSLATION = {
    'A': 'GCT', 'C': 'TGC', 'E': 'GAG', 'D': 'GAC', 'G': 'GGT',
    'F': 'TTC', 'I': 'ATT', 'H': 'CAC', 'K': 'AAG', 'M': 'ATG',
    'L': 'CTA', 'N': 'AAC', 'Q': 'CAG', 'P': 'CCA', 'S': 'TCA',
    'R': 'CGA', 'T': 'ACT', 'W': 'TGG', 'V': 'GTG', 'Y': 'TAC'
}


def translate_aa_to_dna(seq):
    return ''.join([AA_DNA_TRANSLATION.get(x.upper(), '') for x in seq])


"""
A Chaos Representation Grid (CGR) shows the relative frequency of
words (e.g., strings of sequence) in a grid.

The grid is recursively defined as:
C | G
------
A | T

s.t. the lower (A + T) and upper (G + C) halves indicate the base composition
and the diagonals indicate the purine/pyrimidine composition.


E.g., a grid with word length = 2 will be

CC GC | CG GG
AC TC | AG TG
-------------
CA GA | CT GT
AA TA | AT TT

Note that 2 adjacent words differ in only 1 letter
"""


CGR_MAP = {
    'C': lambda (x_min, x_max), (y_min, y_max):
                ((x_min, (x_min + x_max) // 2), (y_min, (y_min + y_max) // 2)),
    'G': lambda (x_min, x_max), (y_min, y_max):
                (((x_min + x_max) // 2, x_max), (y_min, (y_min + y_max) // 2)),
    'A': lambda (x_min, x_max), (y_min, y_max):
                ((x_min, (x_min + x_max) // 2), ((y_min + y_max) // 2, y_max)),
    'T': lambda (x_min, x_max), (y_min, y_max):
                (((x_min + x_max) // 2, x_max), ((y_min + y_max) // 2, y_max)),
}


def words_from_sequence(seq, word_length):
    # sliding window of 1
    for i in xrange(0, len(seq) - word_length + 1):
        word = seq[i:i + word_length]
        yield word


def create_cgr(seq, word_length):
    """ Takes a DNA sequence of {C, G, A, T} and returns its
    Chaos Game Representation (CGR) as a matrix.
    """
    if (set(seq) | {'C', 'G', 'A', 'T'}) != {'C', 'G', 'A', 'T'}:
        raise ValueError("create_cgr takes a DNA sequence."
                         "{0} is not a subset of C, G, A, T".format(str(set(seq))))

    dim = 2**word_length
    # create dim x dim grid
    grid = np.zeros((dim, dim))

    # sliding window of 1
    word_counts = Counter(words_from_sequence(seq, word_length))
    total_word_count = sum(word_counts.values())

    for k, v in word_counts.items():
        # Position the relative frequency in to the CGR grid
        x, y = find_word_coords(k)
        # TODO: should be x, y should work but it gets transposed somewhere..?
        grid[y, x] = v / total_word_count

    return grid


def create_cgr_signature(seq, word_length):
    return create_cgr(seq, word_length).flatten()


def cgr_distance(a, b):
    """ Calculates Euclidean distance between 2 matrices of size p x p,
    representing two CGRs

    See Section 2.4
    """
    if not a.shape == b.shape:
        raise ValueError("a and b should have same shape")
    return np.sqrt(np.sum(np.square(a - b)))


def plot_cgr(cgr):
    # There is a strong distortion in the distribution of values
    # We apply low-pass cutoff and log transformation for better
    # display of the patterns.
    #
    # See:
    # Genomic Signature: Characterization and Classification of
    # Species Assessed by Chaos Game Representation of Sequences

    # - The paper doesn't say what kind of low-pass filter
    # - The paper doesn't say what kind of log transformation
    # => We trial & error'd our own

    def lpf(a):
        _, bin_edges = np.histogram(a, bins=a.shape[0]//10)

        def cutoff(x):
            return bin_edges[1] if x > bin_edges[2] else x
        # Apply the cut off
        a = np.vectorize(cutoff)(a)

        # We need to re-normalize it
        total = np.sum(a)
        return np.vectorize(lambda x: x/total)(a)

    cgr = lpf(cgr)

    with np.errstate(divide='ignore'):  # divide by zero warning
        cgr = np.log(cgr)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cgr, cmap='hot_r')
    fig.colorbar(cax)
    plt.show()


def find_word_coords(word, dim=None):
    dim = dim or 2**len(word)  # The width/height of the (square) grid

    # x and y contain the range of possible coordinates for the word
    x = (0, dim)
    y = (0, dim)

    for l in word.upper()[::-1]:
        x, y = CGR_MAP[l](x, y)

    assert abs(x[0] - x[1]) == 1
    assert abs(y[0] - y[1]) == 1

    return x[0], y[0]