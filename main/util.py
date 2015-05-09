import os
import glob
import random
from itertools import repeat

from cgr import translate_aa_to_dna


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
