#!/usr/bin/env python3
#coding: utf-8

import sys
import itertools
import argparse
from collections import defaultdict, Counter
parser = argparse.ArgumentParser(description="evaluate tagger and/or parser output")
parser.add_argument("goldfile", help="gold annotation conllu file (LL for lang code)")
parser.add_argument("predfile", help="parser output connlu file (LL for lang code)")
parser.add_argument("langsfile", help="file with lang codes")
# TODO mutually exclusive
parser.add_argument("-u", "--upos",
    help="factor output according to UPOS (default)",
    action="store_true")
parser.add_argument("-d", "--deprel",
    help="factor output according to deprel instead of UPOS",
    action="store_true")
# TODO mutually exclusive
parser.add_argument("-p", "--predicted",
    help="factor according to predicted labels (default)",
    action="store_true")
parser.add_argument("-g", "--gold",
    help="factor according to gold labels instead of predicted",
    action="store_true")
args = parser.parse_args()

#UPOS = ['ADJ', 'ADP', 'ADV', 'AUX', 'CONJ', 'DET', 'INTJ', 'NOUN', 'NUM',
#    'PART', 'PRON', 'PROPN', 'PUNCT', 'SCONJ', 'SYM', 'VERB', 'X' ]

# ordered by frequency in en-ud-train.conllu, except for PUNCT which is not
# interesting and therefore pushed down
UPOS = [
       'NOUN', 'VERB', 'PRON', 'ADP', 'DET', 'PROPN', 'ADJ', 'ADV',
       'AUX','PUNCT', 'CONJ', 'PART', 'NUM', 'SCONJ', 'X', 'INTJ', 'SYM'
        ]

# TODO only use the universal ones...
#UDEP = [ 'acl', 'advcl', 'advmod', 'amod', 'appos', 'aux',
#    'auxpass', 'case', 'cc', 'ccomp', 'compound',
#    'conj', 'cop', 'csubj', 'csubjpass', 'dep', 'det',
#    'discourse', 'dislocated', 'dobj', 'expl', 'foreign', 'goeswith', 'iobj',
#    'list', 'mark', 'mwe', 'name', 'neg', 'nmod',
#    'nsubj', 'nsubjpass', 'nummod', 'parataxis', 'punct',
#    'remnant', 'reparandum', 'root', 'vocative', 'xcomp' ]

# ordered by frequency in en-ud-train.conllu
UDEP = [
       'punct', 'nmod', 'case', 'nsubj', 'det', 'root', 'dobj', 'compound',
       'advmod', 'amod', 'conj', 'mark', 'cc', 'aux', 'cop', 'advcl', 'acl',
       'xcomp', 'nummod', 'ccomp', 'neg', 'appos', 'parataxis', 'auxpass',
       'name', 'nsubjpass', 'discourse', 'expl', 'mwe', 'list', 'iobj',
       'csubj', 'goeswith', 'vocative', 'remnant', 'reparandum', 'dep',
       'csubjpass', 'foreign', 'dislocated'
        ]

def next_token(fh):
    while True:
        line = fh.readline()
        if line == '':
            # end of file
            return -1
        elif line.startswith('#') or line.isspace():
            # empty line
            continue
        else:
            # token line
            fields = line.split('\t')
            if not fields[0].isnumeric():
                # multitoken
                continue
            else:
                # regular token
                if args.deprel:
                    # simplify deprel
                    return fields[7].split(':')[0]
                else:
                    # UPOS
                    return fields[3]

# INPUT
results = dict()
with open(args.langsfile, 'r') as langsfile:
    langcodes = [l.rstrip() for l in langsfile.readlines()]
for langcode in langcodes:
    results[langcode] = defaultdict(Counter)
    goldfile = args.goldfile.replace('LL', langcode)
    predfile = args.predfile.replace('LL', langcode)
    gold = open(goldfile, 'r')
    pred = open(predfile, 'r')
    while True:
        gold_label = next_token(gold)
        pred_label = next_token(pred)
        if gold_label == -1 or pred_label == -1:
            # end of file
            if gold_label != pred_label:
                # incorrect end
                sys.exit("ERROR One of the files ended earlier!!!")
            else:
                # correct end
                break
        else:
            if args.gold:
                results[langcode][gold_label][pred_label] += 1
            else:
                results[langcode][pred_label][gold_label] += 1
    gold.close()
    pred.close()
    # convert counts to frequencies
    for label in results[langcode]:
        denominator = sum(results[langcode][label].values())
        for label2 in results[langcode][label]:
            results[langcode][label][label2] /= denominator

# rehash
summed = defaultdict(Counter)
if args.deprel:
    labels = UDEP
else:
    labels = UPOS
for label in labels:
    denominator = 0
    for label2 in labels:
        for langcode in langcodes:
            freq = results[langcode][label][label2];
            summed[label][label2] += freq
            denominator += freq
    if denominator > 0:
        for label2 in labels:
            summed[label][label2] /= denominator


# OUTPUT
for label in labels:
    output = [label]
    for label2 in sorted(summed[label], key=summed[label].get, reverse=True):
        output.append(label2)
        output.append(str(summed[label][label2]))
    print('\t'.join(output))

