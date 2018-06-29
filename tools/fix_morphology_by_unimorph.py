#!/usr/bin/env python3
#coding: utf-8

import sys
import re


feat2conllu = { 'FIN' : 'VerbForm=Fin',
                'NFIN': 'VerbForm=Inf',
                '0'   : 'Person=0',
                '1'   : 'Person=1',
                '2'   : 'Person=2',
                '3'   : 'Person=3',
                '4'   : 'Person=4',
                'SG'  : 'Number=Sing',
                'PL'  : 'Number=Plur',
                'DU'  : 'Number=Dual',
                'N'   : 'Pos=NOUN',
                'V'   : 'Pos=VERB',
                'ADJ' : 'Pos=ADJ',
                'NUM' : 'Pos=NUM',
                'PRS' : 'Tense=Pres',
                'FUT' : 'Tense=Fut',
                'FUT1': 'Tense=Fut',
                'FUT2': 'Tense=Fut',
                'PST' : 'Tence=Past',
                'COND': 'Mood=Cnd',
                'IMP' : 'Mood=Imp',
                'IND' : 'Mood=Ind',
                'SBJV': 'Mood=Sub',
                'MASC': 'Gender=Masc',
                'FEM' : 'Gender=Fem',
                'NEUT': 'Gender=Neut',
                'PFV' : 'Aspect=Perf', # ???
                'PRF' : 'Aspect=Perf', # ???
                'PROG': 'Aspect=Prog',
                'HAB' : 'Aspect=Hab',
                'IPFV': 'Aspect=Imp',
                'DEF' : 'Definite=Fef',
                'INDF': 'Definite=Ind',
                'NOM' : 'Case=Nom',
                'GEN' : 'Case=Gen',
                'DAT' : 'Case=Dat',
                'ACC' : 'Case=Acc',
                'VOC' : 'Case=Voc',
                'LOC' : 'Case=Loc',
                'INS' : 'Case=Ins',
                'ABL' : 'Case=Abl',
                'ESS' : 'Case=Ess',
                'SUB' : 'Case=Sub',
                'NOM/ACC': 'Case=Nom,Acc',
                'ANIM' : 'Animacy:Anim',
                'INAN' : 'Animacy:Inan',
                'POS'  : 'Polarity:Pos',
                'NEG'  : 'Polarity:Neg',
                'PASS' : 'Voice=Pass',

               }
#INST
#LGSPEC1
#LGSPEC2
#PSS1S
#PSS2S
#RES
#SIM Mood=Simulative ??
#V.CONV
#V.CVB
#V.MSDR
#V.PTCP
#V.PTCP.PRS
#V.PTCP.PST

lemma = dict()
morph = dict()

with open(sys.argv[1], 'r') as unimorph_file:
    for line in unimorph_file:
        line = line.strip()
        items = line.split('\t')
        lemma[items[1]] = items[0]
        morph[items[1]] = items[2]
   
for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        if fields[1] in lemma:
            feats_orig = fields[5].split('|')
            feats_unimorph = morph[fields[1]].split(';')
            feats_new = list()
            pos_new = ''
            for feat in feats_unimorph:
                if feat in feat2conllu:
                    if feat2conllu[feat][:4] == 'Pos=':
                        pos_new = feat2conllu[feat][4:]
                    else:
                        feats_new.append(feat2conllu[feat])
            # rewrite POS, lemma, and fetures
            if pos_new != '':
                fields[3] = pos_new
            fields[2] = lemma[fields[1]]
            if len(feats_new) > 0:
                fields[5] = '|'.join(feats_new)
            else:
                fields[5] = '_'
            # TODO: soft rewrite? merge features? sort features?
        print(*fields, sep='\t')
    else:
        print(line)

