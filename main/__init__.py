__author__ = 'tjs'

import os
from cgr import create_cgr, plot_cgr, cgr_dist
from util import translate_aa_to_dna
from classifier import ProteinFamilyClassifier, split_to_train_test


def load_fasta(filename, sequence_transform=None):
    families = []
    sequences = []
    with open(os.path.join('..', 'data', filename), 'r') as f:
        while True:
            info = f.readline().split()
            sequence = f.readline()

            if not sequence:
                break
            # sequence_name = info[0][1:]
            family = info[1].split(';')[1]  # 1 = full name, 0 = code

            families.append(family)
            sequences.append(sequence.rstrip().upper())

    if sequence_transform:
        sequences = map(sequence_transform, sequences)

    return zip(sequences, families)


def load_protein_sequence():
    # TODO: take a *.FASTA file and load a protein sequence
    # PDB  1TJL:A
    return 'MQEGQNRKTSSLSILAIAGVEPYQEKPGEEYMNEAQLAHFRRILEAWRNQLRDEVDRTVTHMQDEAANFPDPVDRAAQEE' + \
            'EFSLELRNRDRERKLIKKIEKTLKKVEDEDFGYCESCGVEIGIRRLEARPTADLCIDCKTLAEIREKQMAG'
    #
    # return 'MFINRWLFSTNHKDIGTLYLLFGAWAGMVGTALSILIRAELGQPGALLGDDQIYNVIVTA' + \
    #        'HAFVMIFFMVMPMMIGGFGNWLVPLMIGAPDMAFPRMNNMSFWLLPPSFLLLLASSMVEA' + \
    #        'GAGTGWTVYPPLAGNLAHAGASVDLTIFSLHLAGVSSILGAINFITTIINMKPPAMTQYQ' + \
    #        'TPLFVWSVLITAVLLLLSLPVLAAGITMLLTDRNLNTTFFDPAGGGDPILYQHLFWFFGH' + \
    #        'PEVYILILPGFGIISHVVTYYSGKKEPFGYMGMVWAMMSIGFLGFIVWAHHMFTVGLDVD' + \
    #        'TRAYFTSATMIIAIPTGVKVFSWLATLHGGNIKWSPAMLWALGFIFLFTVGGLTGIVLSN' + \
    #        'SSLDIVLHDTYYVVAHFHYVLSMGAVFAIMAGFVHWFPLFSGFTLDDTWAKAHFAIMFVG' + \
    #        'VNMTFFPQHFLGLSGMPRRYSDYPDAYTTWNTVSSMGSFISLTAVLIMIFMIWEAFASKR' + \
    #        'EVMSVSYASTNLEWLHGCPPPYHTFEEPTYVKVK'


def load_dna_sequence():
    with open('../data/chromo22.txt', 'r') as fo:
        return ''.join([filter(lambda y: y in 'cgta', x) for line in fo for x in line.split() if not x.isdigit()])


def plot_test(word_length=6):
    dna_seq = load_dna_sequence()
    cgr = create_cgr(dna_seq, word_length)
    plot_cgr(cgr)

if __name__ == '__main__':
    # Load (sequence, family) tuples from FASTA file
    data = load_fasta('16class.fasta',
                      sequence_transform=translate_aa_to_dna)

    training, testing = split_to_train_test(data)

    clf = ProteinFamilyClassifier(word_length=4)
    clf.fit(training)
    metrics = clf.predict(testing)

    for k, v in metrics.items():
        print "{0}: {1}".format(k, v)

