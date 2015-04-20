from __future__ import division

import numpy as np
from sklearn.lda import LDA
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score, \
    accuracy_score

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

        X = np.array(signatures)
        self.clf = LDA()
        self.clf.fit(signatures, families)

       # TODO: maybe return some information about the new feature space ?

    def predict(self, data):
        if not self.clf:
            raise RuntimeError("Cannot call predict before running fit.")

        sequences, true_families = zip(*data)

        # Create signatures from the CGR representations, as our X
        signatures = [create_cgr_signature(seq, self.word_length)
                      for seq in sequences]

        predicted_families = self.clf.predict(signatures)

        precision, recall, fscore, support = precision_recall_fscore_support(
            true_families, predicted_families)

        metrics = {
            'accuracy': accuracy_score(true_families, predicted_families),
            'precision': precision,
            'recall': recall,
            'fscore': fscore,
            'support': support,
            # 'roc_auc': roc_auc_score(true_families, predicted_families),
        }

        return metrics

