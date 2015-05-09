import util

import matplotlib.pyplot as plt

from cgr import create_cgr, plot_cgr, translate_aa_to_dna
from classifier import ProteinFamilyClassifier, ProteinStructureClassifier


def run_cgr_plotter(word_length=8):
    dna_seq = util.load_dna_sequence()
    cgr = create_cgr(dna_seq, word_length)
    plot_cgr(cgr)


def run_protein_family_classifier(training, testing, word_length=4):
    clf = ProteinFamilyClassifier(word_length=word_length)
    clf.fit(training)
    results = clf.predict(testing)

    print "Results for w={0}".format(word_length)
    print results

    # for k, v in metrics.items():
    #     print "{0}: {1}".format(k, v)


def run_protein_structure_classifier():
    clf = ProteinStructureClassifier(num_training=1000)
    clf.load_prototypes(force_recalculate=False)

    sequence = translate_aa_to_dna(util.load_1slva())

    structure, distances, structure_counter = clf.predict_sequence(sequence)
    print structure_counter
    print '=>', structure

    plt.plot(distances)
    plt.show()


if __name__ == '__main__':
    # # Make pretty plots
    run_cgr_plotter(word_length=8)
    #
    # # Protein family classification
    training, testing = util.split_pfam(util.load_pfam())
    run_protein_family_classifier(training, testing, word_length=6)

    # # Protein structure classification
    run_protein_structure_classifier()

    pass  # We comment a lot while trying stuff out
