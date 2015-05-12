import os
import re
import time
import requests

P1_RAW = '1tjlA, 1txuA, 1u19A, 1u7kA, 1u84A, 1vmgA, 1x79B, 1xt0B, 1o5eL, 1qveA, 1r6vA, 1r6yA, 1r7mA, 1s8nA, 1sa3A, 1sbzB, 1sf2B, 1siqA, 1sk9A, 1snyA, 1sw1A, 1sy7A, 1t3qB, 1t3qC, 1t4aA, 1t9mA, 1th0A, 1tjyA, 1tqhA, 1tr0A, 1ts9A, 1tw3A, 1tzlA, 1u00A, 1u0kA, 1u1kA, 1u5hA, 1u69A, 1u7oA, 1u9dA, 1ujmA, 1uliB, 1ulsA, 1uluB, 1um0A, 1ur4A, 1v76A, 1v8mA, 1vc1A, 1vdhA, 1ve6A, 1vggA, 1vkwA, 1vm6A, 1vm7A, 1vmbA, 1vmfA, 1vmjA, 1vp2A, 1vp4A, vp5A, 1vp6A, 1vp8A, 1vzyA, 1w0hA, 1w2cA, 1w4xA, 1wmyA, 11wooA, 1woqA, 1wouA, 1wr8A, x92A, 1x9zA, 1xa1B, 1xebA, 1xfjA, 1xfkA, 1xhkA, 1xhlA, 1xl7B, 1xm3B, 1xm8B, 1xpjA, 1xq6A, 1xrhA, 1xtnA, 1xu7A, 1xuuA, 1qznA, 1u5yA, 1u6dX, 1urlA, 1usqA, 1ux7A, 1wlgA, 1xauA, 1xe1A'  # noqa
CHOU_RAW = '1acyL, 1aep, 1afb1, 1allA, 1amp, 1apyB, 1ash, 1babA, 1babB, 1bafL, 1bbdH, 1bbt2, 1bcfA, 1bgc, 1bgeA, 1bjmA, 1bplA, 1bqlH, 1bqlL, 1cdwA, 1ceo, 1cerO, 1cfb, 1cnt1, 1cnv, 1cof, 1cvl, 1cyw, 1def, 1dfbL, 1div, 1doi, 1dorA, 1eapA, 1edhA, 1emy, 1enp, 1epaB, 1exp, 1fil, 1flp, 1flrH, 1forL, 1fslA, 1gafL, 1gbg, 1gca, 1gdhA, 1gen, 1ggiH, 1ggiL, 1ghfH, 1ghfL, 1ghr, 1ghsA, 1gia, 1gnhA, 1grj, 1gtqA, 1gwp, 1gym, 1hdaA, 1hdaB, 1hdgO, 1hdsA, 1hdsB, 1hilB, 1hjrA, 1hlb, 1hlm, 1hrm, 1htp, 1hup, 1iaiL, 1iaiM, 1ibeA, 1ibeB, 1igcL, 1ikfL, 1ilk, 1indH, 1indL, 1ino, 1itg, 1ithA, 1lbiA, 1lht, 1lit, 1lucA, 1lucB, 1lwiA, 1macA, 1mamL, 1masA, 1maz, 1mbs, 1mfbL, 1mkaA, 1mls, 1mreH, 1msc, 1mygA, 1myt, 1nar, 1ncbL, 1ngqH, 1nhkL, 1nldH, 1npk, 1nsnH, 1nueA, 1obr, 1opgL, 1osa, 1ospL, 1outA, 1outB, 1pbn, 1pbxA, 1pbxB, 1pex, 1pfkA, 1pkp, 1plgH, 1plgL, 1pne, 1poc, 1pvuA, 1qcq, 1rbu, 1rhgA, 1ril, 1sacA, 1sbp, 1sctA, 1sctB, 1scuA, 1seiA, 1sfe, 1snc, 1spgA, 1spgB, 1sra, 1std, 1tcrA, 1tetH, 1tfe, 1thtA, 1trb, 1ula, 1vcaA, 1vdc, 1vgeL, 1vhh, 1vhiA, 1vlk, 1vls, 1vpt, 1vsd, 1whtB, 1wsaA, 1xel, 1xnd, 1xyzA, 1yna, 1ytbA, 1yuhA, 2aak, 2alr, 2asr, 2ayh, 2bgu, 2cgrH, 2ctc, 2ebn, 2fal, 2fbjL, 2gbp, 2gdm, 2hbg, 2jelH, 2kmb1, 2lhb, 2lip, 2mcg1, 2mm1, 2pghA, 2pghB, 2prd, 2tbd, 3ecaA, 3hfmH, 3hhrC, 3pga1, 3sdhA, 4pfk, 6fabL, 7fabH, 7fabL, 8abp, 8atcB, 8fabA, 8fabB, 1agx'  # noqa
NC_RAW = '1wa8A, 1wa8B, 1x3aA, 1x59A, 1z00B, 1z8sA, 1zhcA, 1zzpA, 2a2fX, 2a7oA, 2a7zA, 2ahqA, 2ak6A, 2aplA, 2au5A, 2b8iA, 2c5zA, 2cp8A, 2cprA, 2cqnA, 2crgA, 2d2sA, 2d2yA, 2ddnA, 2es9A, 2etsA, 2f5uA, 2f6hX, 2fj6A, 2fu2A, 2fupA, 2afjA, 2cr9A, 2d9rA, 2f1lA, 2fjlA, 1tvmA, 1u9tA, 1w66A, 1wmmA, 1wpiA, 1wruA, 1wvhA, 1x1fA, 1x52A, 1x53A, 1zc1A, 1zo0A, 1zxfA, 2a2pA, 2a4hA, 2a8eA, 2ae0X, 2ak4A, 2aooA, 2atfA, 2atzA, 2axfA, 2axoA, 2ayuA, 2azeA, 2b20A, 2b59B, 2b61A, 2bdeA, 2bdtA, 2bw2A, 2c0hA, 2c0nA, 2coeA, 2couA, 2cs4A, 2csgA, 2csvA, 2culA, 2cvbA, 2cvnA, 2cw9A, 2cxaA, 2cxzA, 2czrA, 2d08A, 2d1eA, 2exnA, 2f40A, 2f5tX, 2fb6A, 2ffeA, 2fg9A, 2fi1A, 2fpnA, 2fsqA, 2fz0A, 2g0qA, 2g40A, 2g6rA, 1wv3A, 1xt5A, 1y7xA, 1yhpA, 1yntA, 1yntC, 1zeqX, 1zglM, 1zglU, 2ai4A, 2b4wA, 2b8mA, 2bvbA, 2c34A, 2c9aA, 2cewA, 2conA, 2cr2A, 2cryA, 2ersA, 2fb7A'  # noqa

PFAM_RAW = """AA_kinase PF00696
ABC2_membrane PF01061
AMP-binding PF00501
APH PF01636
AAA PF00004
Betalact PF00144
DAO PF01266
DEAD PF00270
DHH PF01368
DHQ_synthase PF01761
E1-E2_ATPase PF00122
ELFV_dehydrog PF00208
Exo_endo_phos PF03372
FA_desaturase PF00487
FtsX PF02687
Glyco_hydro_18 PF00704
Glyco_hydro_31 PF01055
His_biosynth PF00977
Hormone_recep PF00104
Ion_trans PF00520
ketoacyl-synt PF00109
LysR_substrate PF03466
MFS_1 PF07690
Metallophos PF00149
PPDK_N PF01326
Peptidase_C1 PF00112
Peptidase_M14 PF00246
Peptidase_M22 PF00814
peroxidase PF00141
Phos_pyr_kin PF08543
Proteasome PF00227
Pyr_redox_2 PF07992
RNA_pol_L PF01193
RVT_1 PF00078
SBP_bac_5 PF00496
tRNA-synt_2 PF00152
TatD_DNase PF01026
Y_phosphatase PF00102"""

PFAM_TN_RAW = """Autotransporter PF03797
TonB_Dep_Rec PF00593
BPD_transp_1 PF00528
BPD_transp_2 PF02653"""

PFAM = [tuple(map(str.strip, l.split()))
        for l in PFAM_RAW.split('\n') if l]
PFAM_TN = [tuple(map(str.strip, l.split()))
           for l in PFAM_TN_RAW.split('\n') if l]

PDB_URL = 'http://www.rcsb.org/pdb/download/downloadFile.do?' \
          'fileFormat=FASTA&compression=NO&structureId={0}'
PFAM_URL = 'http://pfam.xfam.org/family/{0}/alignment/seed/format?' \
           'format=pfam&alnType=seed&order=t&case=u&gaps=none&download=0'
CATH_URL = 'http://www.cathdb.info/version/latest/domain/{0}'


def prune_chain_label(pdb_id):
    # Returns the pdb_id without the chain label (e.g., '1tjlA' -> '1tjl')
    if pdb_id[-1].isupper():
        return pdb_id[:-1]
    return pdb_id


def download_pdb_sets():
    sets = {
        'P1': map(prune_chain_label, P1_RAW.split(', ')),
        'Chou': map(prune_chain_label, CHOU_RAW.split(', ')),
        'NC': map(prune_chain_label, NC_RAW.split(', ')),
    }

    def download_set(name, pdb_ids):
        print "Downloading {0}, with {1} proteins".format(name, len(pdb_ids))
        data = []
        for i, pdb_id in enumerate(pdb_ids, 1):
            response = requests.get(PDB_URL.format(pdb_id))

            if not response.ok:
                print "Failed: {0} of the set {1}".format(pdb_id, name)
                continue

            data.append(response.text)
            print ' {0}/{1}'.format(i, len(pdb_ids))
            time.sleep(0.1)

        data = ''.join(data)

        # Sequences are broken over lines; we don't want that:
        data = re.sub(r'SEQUENCE', '', data)
        data = re.sub(r'([A-Z])\n([^>])', r'\1\2', data)

        with open(os.path.join('data', name + '.fasta'), 'w') as f:
            f.write(data)

    for set_name, set_pdb_ids in sets.items():
        download_set(set_name, set_pdb_ids)


def download_protein_structures():
    sets = {
        'P1': P1_RAW.split(', '),
        'Chou': CHOU_RAW.split(', '),
        'NC': NC_RAW.split(', '),
    }

    def download_set(name, pdb_ids):
        print "Downloading {0}, with {1} proteins".format(name, len(pdb_ids))
        data = []
        for i, pdb_id in enumerate(pdb_ids, 1):
            response = requests.get(CATH_URL.format(pdb_id + '00'))

            if not response.ok:
                response = requests.get(CATH_URL.format(pdb_id + '01'))

            if not response.ok:
                print "Failed: {0} of the set {1}".format(pdb_id, name)
                continue

            if 'Mainly Alpha' in response.text:
                structural_class = 'Mainly Alpha'
            elif 'Mainly Beta' in response.text:
                structural_class = 'Mainly Beta'
            elif 'Alpha Beta' in response.text:
                structural_class = 'Alpha Beta'
            else:
                print "No structure found: {0} " \
                      "of the set {1}".format(pdb_id, name)
                continue

            data.append('{0}, {1}'.format(pdb_id, structural_class))

            print ' {0}/{1}'.format(i, len(pdb_ids))
            time.sleep(0.1)

        data = '\n'.join(data)

        with open(os.path.join('data', name + '.structure'), 'w') as f:
            f.write(data)

    download_set('Chou', sets['Chou'])


def download_pfam_set(pfam_name, families):

    for i, (family_name, pfam_id) in enumerate(families, 1):
        print "Downloading {0}, {1}/{2}".format(family_name, i, len(families))

        response = requests.get(PFAM_URL.format(pfam_id))

        if not response.ok:
            print "Failed: {0} ({1})".format(family_name, pfam_id)
            continue

        with open(os.path.join('data', pfam_name, family_name + '.pfam'), 'w')\
                as f:
            f.write(response.text)

        time.sleep(2)


if __name__ == '__main__':
    # download_pdb_sets()
    # download_pfam_set('Pfam', PFAM)
    # download_pfam_set('Pfam-TN', PFAM_TN)
    download_protein_structures()
    pass
