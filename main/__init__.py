import util

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


def run_protein_structure_classifier(data):
    clf = ProteinStructureClassifier(num_training=2500)
    clf.load_prototypes(force_recalculate=False)

    confusion_matrix = clf.predict(data)

    print confusion_matrix


def load_fasta_structure():
    pass
    # data = util.load_fasta(dataset + '.fasta',
    #                        sequence_transform=translate_aa_to_dna,
    #                        with_chain_label=True)
    #
    # data = filter(lambda x: x[1].lower() in FILTER_LIST[dataset], data)
    # sequences = zip(*data)[0]
    # print len(sequences)

if __name__ == '__main__':
    # # Make pretty plots
    # run_cgr_plotter(word_length=8)
    #
    # # Protein family classification
    # training, testing = util.split_pfam(util.load_pfam())
    # run_protein_family_classifier(training, testing, word_length=6)

    # # Protein structure classification
    run_protein_structure_classifier(util.load_1189())
    # run_protein_structure_classifier(util.load_sequence_with_structure('P1'))

    pass  # We comment a lot while trying stuff out
