#!/usr/bin/env python3
#coding: utf-8

import sys
import itertools
import argparse
parser = argparse.ArgumentParser(description="evaluate tagger and/or parser output")
parser.add_argument("goldfile", help="gold annotation conllu file")
parser.add_argument("predfile", help="parser output connlu file")
parser.add_argument("-m", "--measure",
    help="accuracy of what to measure",
    choices=['pos', 'head', 'deprel', 'las'],
    default='las')
# TODO mutually exclusive
parser.add_argument("-u", "--posfactored",
    help="factor output according to UPOS (default)",
    action="store_true")
parser.add_argument("-d", "--deprelfactored",
    help="factor output according to deprel instead of UPOS",
    action="store_true")
# TODO mutually exclusive
parser.add_argument("-p", "--predicted",
    help="factor according to predicted labels (default)",
    action="store_true")
parser.add_argument("-g", "--gold",
    help="factor according to gold labels instead of predicted",
    action="store_true")
# TODO mutually exclusive
parser.add_argument("-a", "--accuracy",
    help="individual accuracy (default)",
    action="store_true")
parser.add_argument("-e", "--errorshare",
    help="share of total error instead of individual accuracy",
    action="store_true")
parser.add_argument("-j", "--joined",
    help="joined nonfactored eval",
    action="store_true")
parser.add_argument("-c", "--columns",
    help="print header listing the column labels first",
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

class Evaluation:
    total = 0
    pos_good = 0
    head_good = 0
    deprel_good = 0
    las_good = 0
    
    def add(self, pos_good, head_good, deprel_good, las_good):
        self.total += 1
        if pos_good:
            self.pos_good += 1
        if head_good:
            self.head_good += 1
        if deprel_good:
            self.deprel_good += 1
        if las_good:
            self.las_good += 1
    
    def get(self, count):
        if self.total > 0:
            return count/self.total
        else:
            return ''

    def get_pos(self):
        return self.get(self.pos_good)
    
    def get_head(self):
        return self.get(self.head_good)
    
    def get_deprel(self):
        return self.get(self.deprel_good)

    def get_las(self):
        return self.get(self.las_good)

    def get_named(self, name="las"):
        if name == 'pos':
            return self.get_pos()
        elif name == 'head':
            return self.get_head()
        elif name == 'deprel':
            return self.get_deprel()
        else:
            return self.get_las()

    def get_named_error_count(self, name="las"):
        if name == 'pos':
            return self.total - self.pos_good
        elif name == 'head':
            return self.total - self.head_good
        elif name == 'deprel':
            return self.total - self.deprel_good
        else:
            return self.total - self.las_good

# Init
evaluation_all = Evaluation()
evaluation_gold = dict()
evaluation_pred = dict()
for label in itertools.chain(UPOS, UDEP):
    evaluation_gold[label] = Evaluation()
    evaluation_pred[label] = Evaluation()

def next_token(fh):
    while True:
        line = fh.readline()
        if line == '':
            # end of file
            return (-1, -1, -1)
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
                # simplify deprel
                deprel = fields[7].split(':')[0]
                # UPOS, head, deprel
                return (fields[3], fields[6], deprel)

def evaluate(gold_pos, gold_head, gold_deprel,
        pred_pos, pred_head, pred_deprel):
    pos_good = gold_pos == pred_pos
    head_good = gold_head == pred_head
    deprel_good = gold_deprel == pred_deprel
    las_good = head_good and deprel_good
    return (pos_good, head_good, deprel_good, las_good)

# INPUT
gold = open(args.goldfile, 'r')
pred = open(args.predfile, 'r')
while True:
    (gold_pos, gold_head, gold_deprel) = next_token(gold)
    (pred_pos, pred_head, pred_deprel) = next_token(pred)
    if gold_pos == -1 or pred_pos == -1:
        # end of file
        if gold_pos != pred_pos:
            # incorrect end
            sys.exit("ERROR One of the files ended earlier!!!")
        else:
            # correct end
            break
    else:
        evaluation_tuple = evaluate(
                gold_pos, gold_head, gold_deprel,
                pred_pos, pred_head, pred_deprel)
        evaluation_all.add(*evaluation_tuple)
        evaluation_gold[gold_pos].add(*evaluation_tuple)
        evaluation_gold[gold_deprel].add(*evaluation_tuple)
        evaluation_pred[pred_pos].add(*evaluation_tuple)
        evaluation_pred[pred_deprel].add(*evaluation_tuple)
gold.close()
pred.close()

# OUTPUT
if args.joined:
    print(evaluation_all.get_named(args.measure))
else:
    if args.deprelfactored:
        labels = UDEP
    else:
        labels = UPOS
    if args.errorshare:
        if args.gold:
            errors = [evaluation_gold[label].get_named_error_count(args.measure)
                    for label in labels]
        else:
            errors = [evaluation_pred[label].get_named_error_count(args.measure)
                    for label in labels]
        total_errors = sum(errors)
        output = [str(error/total_errors) for error in errors]
    else:
        if args.gold:
            output = [str(evaluation_gold[label].get_named(args.measure))
                    for label in labels]
        else:
            output = [str(evaluation_pred[label].get_named(args.measure))
                    for label in labels]
    if args.columns:
        print('\t'.join(labels))
    print('\t'.join(output))

