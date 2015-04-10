__author__ = 'tjs'

from cgr import create_cgr, plot_cgr
from util import translate_aa_to_dna


def load_protein_sequence():
    # TODO: take a *.FASTA file and load a protein sequence
    return 'MFINRWLFSTNHKDIGTLYLLFGAWAGMVGTALSILIRAELGQPGALLGDDQIYNVIVTA' + \
           'HAFVMIFFMVMPMMIGGFGNWLVPLMIGAPDMAFPRMNNMSFWLLPPSFLLLLASSMVEA' + \
           'GAGTGWTVYPPLAGNLAHAGASVDLTIFSLHLAGVSSILGAINFITTIINMKPPAMTQYQ' + \
           'TPLFVWSVLITAVLLLLSLPVLAAGITMLLTDRNLNTTFFDPAGGGDPILYQHLFWFFGH' + \
           'PEVYILILPGFGIISHVVTYYSGKKEPFGYMGMVWAMMSIGFLGFIVWAHHMFTVGLDVD' + \
           'TRAYFTSATMIIAIPTGVKVFSWLATLHGGNIKWSPAMLWALGFIFLFTVGGLTGIVLSN' + \
           'SSLDIVLHDTYYVVAHFHYVLSMGAVFAIMAGFVHWFPLFSGFTLDDTWAKAHFAIMFVG' + \
           'VNMTFFPQHFLGLSGMPRRYSDYPDAYTTWNTVSSMGSFISLTAVLIMIFMIWEAFASKR' + \
           'EVMSVSYASTNLEWLHGCPPPYHTFEEPTYVKVK'


def load_dna_sequence():
    with open('../data/chromo22.txt', 'r') as fo:
        return ''.join([filter(lambda y: y in 'cgta', x) for line in fo for x in line.split() if not x.isdigit()])


if __name__ == '__main__':
    # dna_seq = translate_aa_to_dna(load_protein_sequence())
    dna_seq = load_dna_sequence()

    cgr = create_cgr(dna_seq, 7)
    plot_cgr(cgr)

