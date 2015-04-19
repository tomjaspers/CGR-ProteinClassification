# Translation from Amino Acids to DNA, as described in Section 2.2
AA_DNA_TRANSLATION = {
    'A': 'GCT', 'C': 'TGC', 'E': 'GAG', 'D': 'GAC', 'G': 'GGT',
    'F': 'TTC', 'I': 'ATT', 'H': 'CAC', 'K': 'AAG', 'M': 'ATG',
    'L': 'CTA', 'N': 'AAC', 'Q': 'CAG', 'P': 'CCA', 'S': 'TCA',
    'R': 'CGA', 'T': 'ACT', 'W': 'TGG', 'V': 'GTG', 'Y': 'TAC'
}


def translate_aa_to_dna(seq):
    return ''.join([AA_DNA_TRANSLATION.get(x.upper(), '') for x in seq])


