__author__ = 'tjs'

from cgr import create_cgr, plot_cgr, create_cgr_signature, translate_aa_to_dna
from classifier import ProteinFamilyClassifier
from util import *


def run_cgr_plotter(word_length=8):
    dna_seq = load_dna_sequence()
    cgr = create_cgr(dna_seq, word_length)
    plot_cgr(cgr)


def run_protein_family_classifier(training, testing, word_length=4):
    clf = ProteinFamilyClassifier(word_length=word_length)
    clf.fit(training)
    metrics = clf.predict(testing)

    for k, v in metrics.items():
        print "{0}: {1}".format(k, v)


if __name__ == '__main__':
    # Make pretty plots
    # run_cgr_plotter(word_length=7)

    # Protein family classification
    training, testing = split_to_train_test(
        load_fasta('random/16class.fasta',
                   sequence_transform=translate_aa_to_dna))
    # training, testing = split_pfam(load_pfam())
    run_protein_family_classifier(training, testing, word_length=4)

    # We comment a lot while trying stuff out
    pass


