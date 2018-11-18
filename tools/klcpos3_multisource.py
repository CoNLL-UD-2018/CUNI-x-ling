#!/usr/bin/env python3
#coding: utf-8

from math import log
import sys
import gzip
from collections import deque, defaultdict

# compute D_KL(P||Q)
# i.e. we approximate P by Q
# projection from lang1 to lang2

import argparse
parser = argparse.ArgumentParser(
        description="compute KLcpos3 distance of source and target tagged data")
parser.add_argument("tgtfile", help="target connlu file")
parser.add_argument("srcfile", nargs='+', help="source conllu file")
parser.add_argument("-F", "--formula", type=int,
        help="formula: 0=kl, 1=-kl, 2=kl+kl2, 3=kl+hyp, 4=kl+kl2+hyp",
        default=0)
parser.add_argument("-S", "--smooth", type=float,
    help="add S smoothing (default=0.5)", default=0.5)
parser.add_argument("-l", "--linsmooth",
    help="linear interpolation smoothing: 1+10KL1+100KL2+1000KL3+...",
    action="store_true")
parser.add_argument("-w", "--weightdown",
    help="weight down lower ngrams in linear interpol smoothing",
    action="store_true")
parser.add_argument("-i", "--inverse",
    help="compute the inverse (KLcpos3^-4), to be used as similarity measure",
    action="store_true")
parser.add_argument("-N", type=int,
    help="ngram length (default=3)", default=3)
parser.add_argument("-P", "--postags", type=int,
    help="number of POS tags (default=18)", default=18)
parser.add_argument("-s", "--sep", type=str,
        help="separator of values on output (default=tab)", default='\t')
args = parser.parse_args()

if args.sep == '\\n':
    args.sep = '\n'

END = 'BOUNDARY'

def new_ngram_deque():
    return deque(args.N * [END])

def countngram(dictionary, ngram):
    for start in range(args.N):
        length = args.N-start
        part = tuple(list(ngram)[start:])
        dictionary[length][part] += 1

# read counts from files
def readfile(filename):
    result = [defaultdict(int) for n in range(args.N+1)]
    result[0][()] = 1
    sentence_count = 0
    if filename.endswith(".gz"):
        inputfile = gzip.open(filename, 'rt', encoding='utf-8')
    else:
        inputfile = open(filename, 'r')
    ngram = new_ngram_deque()
    
    for line in inputfile:
        line = line.strip()
        if line == '':
            # end of sentence
            sentence_count += 1
            for i in range(args.N-1):
                ngram.popleft()
                ngram.append(END)
                countngram(result, ngram)
        elif line.startswith('#'):
            # ignore comments
            continue
        else:
            fields = line.split('\t')
            # skip special tokens
            if fields[0].isdigit():
                ngram.popleft()
                tag = fields[3]
                ngram.append(tag)
                countngram(result, ngram)
            # else continue

    inputfile.close()
    return (result, sentence_count)

def kl2invkl4(kl):
    return kl**-4

def klcpos3(target_counts, source_counts):
    # corpus size
    target_sum = sum(target_counts[args.N].values())
    source_sum = sum(source_counts[args.N].values())
    
    dkl = 0
    if args.linsmooth:
        # add args.S smoothing for unigrams
        for ngram in target_counts[1]:
            if not ngram in source_counts[1]:
                source_counts[1][ngram] = args.smooth
                source_sum += args.smooth
        # get smoother dkl for all ngrams
        for ngram in target_counts[args.N]:
            # target prob is unsmoothed
            target_prob = target_counts[args.N][ngram]/target_sum 
            # init by N-gram prob
            source_prob = source_counts[args.N][ngram]/source_sum 
            # go over all lower mgrams
            for m in range(1, args.N):
                # there are overlaps, so boost each by (m-1)*(n-m+1)
                # TODO some bug here
                m_prob = args.postags**((m-1)*(args.N-m))
                # m_prob = 1
                # go over all positions of the mgram
                for start in range(args.N-m+1):
                    mgram = tuple(ngram[start:start+m])
                    m_prob *= source_counts[m][mgram]/source_sum 
                # weight down
                if (args.weightdown):
                    source_prob += m_prob/(10**(args.N-m))
                else:
                    source_prob += m_prob
            # average
            # source_prob /= args.N
            # dkl
            dkl += target_prob * log(target_prob/source_prob)
    else:
        # add args.S smoothing
        for ngram in target_counts[args.N]:
            if not ngram in source_counts[args.N]:
                source_counts[args.N][ngram] = args.smooth
                source_sum += args.smooth
        # compute D_kl
        for ngram in target_counts[args.N]:
            target_prob = target_counts[args.N][ngram]/target_sum 
            source_prob = source_counts[args.N][ngram]/source_sum 
            dkl += target_prob * log(target_prob/source_prob)
    # output
    return dkl

def apply_transform(kl, sentence_count):
    hyp35 = 1/(sentence_count+35)
    formulas = [kl,
            -10.9*kl + 54,
            -19.0*kl + 1.85*kl*kl + 61,
            -10.9*kl -  560*hyp35 + 55.9,
            -19.0*kl + 1.85*kl*kl - 560*hyp35 + 62.8,
            ]
    return formulas[args.formula]


# MAIN

# the language we want to parse (P)
target_counts, _ = readfile(args.tgtfile)

result = list()
for source in args.srcfile:
    # the source language which we use to train the parser (Q)
    source_counts, source_sentence_count = readfile(source)
    dkl = klcpos3(target_counts, source_counts)
    sim = apply_transform(dkl, source_sentence_count)
    if args.inverse:
        result.append(kl2invkl4(sim))
    else:
        result.append(sim)
print(*result, sep=args.sep)

