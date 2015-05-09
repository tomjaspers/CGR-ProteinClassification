from __future__ import division

import os
import pickle
from collections import Counter

import numpy as np
from sklearn.lda import LDA
from sklearn.metrics import classification_report

from main.cgr import create_cgr, create_cgr_signature, cgr_distance, \
    translate_aa_to_dna


class ProteinFamilyClassifier(object):

    def __init__(self, word_length):
        self.word_length = word_length
        self.clf = None

    def fit(self, data):
        sequences, families = zip(*data)

        # Create signatures from the CGR representations, as our X
        signatures = [create_cgr_signature(seq, self.word_length)
                      for seq in sequences]

        self.clf = LDA()
        self.clf.fit(np.array(signatures), families)

        # TODO: maybe return some information about the new feature space ?

    def predict(self, data):
        if not self.clf:
            raise RuntimeError("Cannot call predict before running fit.")

        sequences, true_families = zip(*data)

        # Create signatures from the CGR representations, as our X
        signatures = [create_cgr_signature(seq, self.word_length)
                      for seq in sequences]

        predicted_families = self.clf.predict(signatures)

        # precision, recall, fscore, support = precision_recall_fscore_support(
        #     true_families, predicted_families)
        #
        # confusion_matrix = \
        #     confusion_matrix(true_families, predicted_families)
        #
        # metrics = {
        #     'accuracy': accuracy_score(true_families, predicted_families),
        #     'precision': precision,
        #     'recall': recall,
        #     'fscore': fscore,
        #     'support': support,
        #     'confusion_matrix': confusion_matrix,
        #     # 'roc_auc': roc_auc_score(true_families, predicted_families),
        # }

        return classification_report(true_families, predicted_families)


class ProteinStructureClassifier(object):

    def __init__(self, word_length=6, num_training=500, window_size=75):
        self.word_length = word_length  # default from paper, Section 2.5.2
        self.window_size = window_size  # default from paper, Section 2.5.5

        self.unstructured_threshold_percentage = 0.1  # Section 2.5.4

        # number of proteins to use for generating signature
        self.num_mainly_alphas = self.num_mainly_betas = num_training

        self.alpha_prototype = None
        self.beta_prototype = None

    def load_prototypes(self, force_recalculate=False):
        """ Load the prototype signatures for mainly alpha and mainly beta.

        It will try to attempt to load the signatures from a pickle file if
        force_recalculate is set to False.

        If the pickle file cannot be loaded or force_recalculate is set to True
        then it will use the CATH dataset to generate them, and save.
        If a pickle file is passed, it will load from there, if not, it will
        use the CATH dataset to generate them (and save this as pickle).
        """
        def pickle_filename():
            return '../data/pickles/nA{0}_nB{1}_w{2}_l{3}.pickle'.format(
                self.num_mainly_alphas,
                self.num_mainly_betas,
                self.word_length,
                self.window_size)

        if not force_recalculate:
            try:
                with open(pickle_filename(), 'r') as p:
                    self.alpha_prototype, self.beta_prototype = pickle.load(p)
                loaded_pickle = True
            except (IOError, TypeError, pickle.PickleError) as e:
                print e
                loaded_pickle = False
        else:
            loaded_pickle = False

        if not loaded_pickle:
            print "Calculating"
            self.alpha_prototype, self.beta_prototype = \
                self._create_alpha_beta_prototype_structures()
            with open(pickle_filename(), 'w') as p:
                pickle.dump((self.alpha_prototype, self.beta_prototype), p)

    def predict_sequence(self, sequence):
        # We have to pad the end of the DNA sequence with a series of adenines
        if not isinstance(sequence, str):
            raise TypeError("Sequence should be a DNA string")

        # sequence = sequence.ljust(len(sequence)//self.window_size + 1, 'A')
        sequence += 'A'*self.window_size

        distances = []
        for i in xrange(0, len(sequence)-self.window_size):
            window = sequence[i:i+self.window_size]
            # TODO: not sure if this is needed
            if len(window) < self.window_size:
                break
            window_signature = create_cgr(window, self.word_length)

            d_alpha = cgr_distance(self.alpha_prototype, window_signature)
            d_beta = cgr_distance(self.beta_prototype, window_signature)

            distance = d_alpha - d_beta
            distances.append(distance)

        max_distance_range = max(distances) - min(distances)
        unstructured_threshold = \
            max_distance_range * self.unstructured_threshold_percentage

        structure_counter = Counter()
        for dist in distances:
            if dist > unstructured_threshold:
                structure_counter['beta'] += 1
            elif dist < -1*unstructured_threshold:
                structure_counter['alpha'] += 1
            else:
                # -threshold <= distance <= threshold
                structure_counter['unstructured'] += 1

        # See 2.5.5
        if structure_counter['beta'] < 3 or structure_counter['alpha'] < 5:
            structure = 'Unstructured'
        else:
            if structure_counter['alpha'] > structure_counter['beta']:
                structure = 'Mostly alpha'
            else:
                structure = 'Mostly beta'

        return structure, distances, structure_counter

    def predict(self, data):
        pass

    def _create_alpha_beta_prototype_structures(self):
        """ Create signature representatives (prototypes) of alpha and beta classes

          We use the CATH-set
          First, we generated a CGR for each sequence. Then, we used a
          discriminant analysis to identify the signatures' representative of
          the two structural classes.
        See Section 2.5.2
        :return: CGR for the alpha prototype, CGR for the beta prototype
        """

        # Map the PDB_IDs per Class
        pdb_ids_per_class = {
            1: set(),  # Mainly Alpha
            2: set(),  # Mainly Beta
            3: set(),  # Alpha-Beta
            4: set(),  # Few Secondary Structures
        }

        # CathDomainList contains a mapping of the PDB Code with the class code
        with open(os.path.join('..', 'data', 'CATH', 'CathDomainList.txt')) \
                as f:
            for line in f:
                pdb_id, class_code = line.split()[:2]
                pdb_ids_per_class[int(class_code)].add(pdb_id)

        # Map the sequences per class
        sequences_per_class = {
            1: [],
            2: [],
            3: [],
            4: [],
        }

        # CathDomainSeqs contains line pairs holding the info and the sequence
        with open(os.path.join('..', 'data', 'CATH', 'CathDomainSeqs.txt')) \
                as f:
            while True:
                info = f.readline().split('|')
                sequence = f.readline()

                if not sequence:
                    break

                pdb_id = info[1].strip()

                # For now, we only care about mainly alphas and mainly betas
                for class_code in [1, 2]:
                    if pdb_id in pdb_ids_per_class[class_code]:
                        sequences_per_class[class_code].append(sequence)
                        continue

        assert len(pdb_ids_per_class[1]) == len(sequences_per_class[1])
        assert len(pdb_ids_per_class[2]) == len(sequences_per_class[2])

        mainly_alphas = [
            create_cgr_signature(translate_aa_to_dna(seq), self.word_length)
            for seq in list(sequences_per_class[1])[:self.num_mainly_alphas]]
        mainly_betas = [
            create_cgr_signature(translate_aa_to_dna(seq), self.word_length)
            for seq in list(sequences_per_class[2])[:self.num_mainly_betas]]

        clf = LDA()
        x = np.array(mainly_alphas + mainly_betas)
        y = np.array([1]*self.num_mainly_alphas + [2]*self.num_mainly_betas)
        clf.fit(x, y)

        # Note that the means will just be a 2^(word_length+1) array, which we
        # needs to transform back to a 2^word_length x 2^word_length array
        dim = 2**self.word_length
        alpha_prototype = np.reshape(clf.means_[0], (dim, dim))
        beta_prototype = np.reshape(clf.means_[1], (dim, dim))

        return alpha_prototype, beta_prototype
