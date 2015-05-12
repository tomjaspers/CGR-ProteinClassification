import os
import glob
import random
from itertools import repeat

from cgr import translate_aa_to_dna

P1_RAW = '1tjlA, 1txuA, 1u19A, 1u7kA, 1u84A, 1vmgA, 1x79B, 1xt0B, 1o5eL, 1qveA, 1r6vA, 1r6yA, 1r7mA, 1s8nA, 1sa3A, 1sbzB, 1sf2B, 1siqA, 1sk9A, 1snyA, 1sw1A, 1sy7A, 1t3qB, 1t3qC, 1t4aA, 1t9mA, 1th0A, 1tjyA, 1tqhA, 1tr0A, 1ts9A, 1tw3A, 1tzlA, 1u00A, 1u0kA, 1u1kA, 1u5hA, 1u69A, 1u7oA, 1u9dA, 1ujmA, 1uliB, 1ulsA, 1uluB, 1um0A, 1ur4A, 1v76A, 1v8mA, 1vc1A, 1vdhA, 1ve6A, 1vggA, 1vkwA, 1vm6A, 1vm7A, 1vmbA, 1vmfA, 1vmjA, 1vp2A, 1vp4A, vp5A, 1vp6A, 1vp8A, 1vzyA, 1w0hA, 1w2cA, 1w4xA, 1wmyA, 11wooA, 1woqA, 1wouA, 1wr8A, x92A, 1x9zA, 1xa1B, 1xebA, 1xfjA, 1xfkA, 1xhkA, 1xhlA, 1xl7B, 1xm3B, 1xm8B, 1xpjA, 1xq6A, 1xrhA, 1xtnA, 1xu7A, 1xuuA, 1qznA, 1u5yA, 1u6dX, 1urlA, 1usqA, 1ux7A, 1wlgA, 1xauA, 1xe1A'  # noqa
CHOU_RAW = '1acyL, 1aep, 1afb1, 1allA, 1amp, 1apyB, 1ash, 1babA, 1babB, 1bafL, 1bbdH, 1bbt2, 1bcfA, 1bgc, 1bgeA, 1bjmA, 1bplA, 1bqlH, 1bqlL, 1cdwA, 1ceo, 1cerO, 1cfb, 1cnt1, 1cnv, 1cof, 1cvl, 1cyw, 1def, 1dfbL, 1div, 1doi, 1dorA, 1eapA, 1edhA, 1emy, 1enp, 1epaB, 1exp, 1fil, 1flp, 1flrH, 1forL, 1fslA, 1gafL, 1gbg, 1gca, 1gdhA, 1gen, 1ggiH, 1ggiL, 1ghfH, 1ghfL, 1ghr, 1ghsA, 1gia, 1gnhA, 1grj, 1gtqA, 1gwp, 1gym, 1hdaA, 1hdaB, 1hdgO, 1hdsA, 1hdsB, 1hilB, 1hjrA, 1hlb, 1hlm, 1hrm, 1htp, 1hup, 1iaiL, 1iaiM, 1ibeA, 1ibeB, 1igcL, 1ikfL, 1ilk, 1indH, 1indL, 1ino, 1itg, 1ithA, 1lbiA, 1lht, 1lit, 1lucA, 1lucB, 1lwiA, 1macA, 1mamL, 1masA, 1maz, 1mbs, 1mfbL, 1mkaA, 1mls, 1mreH, 1msc, 1mygA, 1myt, 1nar, 1ncbL, 1ngqH, 1nhkL, 1nldH, 1npk, 1nsnH, 1nueA, 1obr, 1opgL, 1osa, 1ospL, 1outA, 1outB, 1pbn, 1pbxA, 1pbxB, 1pex, 1pfkA, 1pkp, 1plgH, 1plgL, 1pne, 1poc, 1pvuA, 1qcq, 1rbu, 1rhgA, 1ril, 1sacA, 1sbp, 1sctA, 1sctB, 1scuA, 1seiA, 1sfe, 1snc, 1spgA, 1spgB, 1sra, 1std, 1tcrA, 1tetH, 1tfe, 1thtA, 1trb, 1ula, 1vcaA, 1vdc, 1vgeL, 1vhh, 1vhiA, 1vlk, 1vls, 1vpt, 1vsd, 1whtB, 1wsaA, 1xel, 1xnd, 1xyzA, 1yna, 1ytbA, 1yuhA, 2aak, 2alr, 2asr, 2ayh, 2bgu, 2cgrH, 2ctc, 2ebn, 2fal, 2fbjL, 2gbp, 2gdm, 2hbg, 2jelH, 2kmb1, 2lhb, 2lip, 2mcg1, 2mm1, 2pghA, 2pghB, 2prd, 2tbd, 3ecaA, 3hfmH, 3hhrC, 3pga1, 3sdhA, 4pfk, 6fabL, 7fabH, 7fabL, 8abp, 8atcB, 8fabA, 8fabB, 1agx'  # noqa
NC_RAW = '1wa8A, 1wa8B, 1x3aA, 1x59A, 1z00B, 1z8sA, 1zhcA, 1zzpA, 2a2fX, 2a7oA, 2a7zA, 2ahqA, 2ak6A, 2aplA, 2au5A, 2b8iA, 2c5zA, 2cp8A, 2cprA, 2cqnA, 2crgA, 2d2sA, 2d2yA, 2ddnA, 2es9A, 2etsA, 2f5uA, 2f6hX, 2fj6A, 2fu2A, 2fupA, 2afjA, 2cr9A, 2d9rA, 2f1lA, 2fjlA, 1tvmA, 1u9tA, 1w66A, 1wmmA, 1wpiA, 1wruA, 1wvhA, 1x1fA, 1x52A, 1x53A, 1zc1A, 1zo0A, 1zxfA, 2a2pA, 2a4hA, 2a8eA, 2ae0X, 2ak4A, 2aooA, 2atfA, 2atzA, 2axfA, 2axoA, 2ayuA, 2azeA, 2b20A, 2b59B, 2b61A, 2bdeA, 2bdtA, 2bw2A, 2c0hA, 2c0nA, 2coeA, 2couA, 2cs4A, 2csgA, 2csvA, 2culA, 2cvbA, 2cvnA, 2cw9A, 2cxaA, 2cxzA, 2czrA, 2d08A, 2d1eA, 2exnA, 2f40A, 2f5tX, 2fb6A, 2ffeA, 2fg9A, 2fi1A, 2fpnA, 2fsqA, 2fz0A, 2g0qA, 2g40A, 2g6rA, 1wv3A, 1xt5A, 1y7xA, 1yhpA, 1yntA, 1yntC, 1zeqX, 1zglM, 1zglU, 2ai4A, 2b4wA, 2b8mA, 2bvbA, 2c34A, 2c9aA, 2cewA, 2conA, 2cr2A, 2cryA, 2ersA, 2fb7A'  # noqa

FILTER_LIST = {
    'P1': map(str.lower, set(P1_RAW.split(', '))),
    'Chou': map(str.lower, set(CHOU_RAW.split(', '))),
    'NC': map(str.lower, set(NC_RAW.split(', '))),
}


def split_to_train_test(data, ratio=0.70):
    random.shuffle(data)
    split_point = int(len(data) * ratio)

    train, test = data[:split_point], data[split_point:]

    assert len(train)+len(test) == len(data)

    return train, test


def load_pfam():
    data = {}
    for family_path in glob.glob('../data/Pfam/*.pfam'):
        # This is kinda dirty, but works for now
        family_name = family_path.split('/')[-1].split('.')[0]
        with open(family_path, 'r') as f:
            data[family_name] = [translate_aa_to_dna(l.split()[1]) for l in f]
    return data


def split_pfam(data, ratio=0.8):
    training = []
    testing = []

    for family, sequences in data.items():
        random.shuffle(sequences)
        split_point = int(len(sequences) * ratio)

        train, test = sequences[:split_point], sequences[split_point:]

        training.extend(zip(train, repeat(family, len(train))))
        testing.extend(zip(test, repeat(family, len(test))))

    return training, testing


def load_fasta(filename, sequence_transform=None, with_chain_label=False):
    families = []
    sequences = []
    with open(os.path.join('..', 'data', filename), 'r') as f:
        while True:
            info = f.readline().split()
            sequence = f.readline()

            if not sequence:
                break
            # sequence_name = info[0][1:]
            try:
                family = info[1].split(';')[1]  # 1 = full name, 0 = code
            except IndexError:
                split_info = info[0].split(':')
                if not with_chain_label:
                    family = split_info[0][1:]
                else:
                    family = ''.join(split_info)[1:].split('|')[0]


            families.append(family)
            sequences.append(sequence.rstrip().upper())

    if sequence_transform:
        sequences = map(sequence_transform, sequences)

    return set(zip(sequences, families))


def load_structure(filename):
    structure_map = {}
    with open(os.path.join('..', 'data', filename), 'r') as f:
        for line in f:
            pdb_id_with_chain, structure = map(str.strip, line.split(', '))
            structure_map[pdb_id_with_chain.lower()] = structure
    return structure_map


def load_sequence_with_structure(name):
    data = []
    fasta_data = load_fasta(
        name + '.fasta',
        sequence_transform=translate_aa_to_dna,
        with_chain_label=True)
    structure_map = load_structure(name + '.structure')
    for sequence, pdb_id in fasta_data:
        structure = structure_map.get(pdb_id.lower())
        if structure:
            data.append((sequence, structure))

    return data


def load_1189():
    data = []

    with open(os.path.join('..', 'data', '1189.dta'), 'r') as f:
        for line in f:
            line = line.split(', ')
            # (sequence , true classification)
            data.append((translate_aa_to_dna(line[2].strip()), line[1]))

    return data