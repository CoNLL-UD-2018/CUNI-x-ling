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
parser.add_argument("srcfile", help="source conllu file")
parser.add_argument("tgtfile", help="target connlu file")
parser.add_argument("-i", "--inverse",
    help="compute the inverse (KLcpos3^-4), to be used as similarity measure",
    action="store_true")
parser.add_argument("-N", type=int,
    help="ngram length (default=3)", default=3)
args = parser.parse_args()

END = 'BOUNDARY'
SMOOTH = 0.5

def new_ngram_deque():
    return deque(args.N * [END])

# read counts from files
def readfile(filename):
    result = defaultdict(int)
    if filename.endswith(".gz"):
        inputfile = gzip.open(filename, 'rt', encoding='utf-8')
    else:
        inputfile = open(filename, 'r')
    ngram = new_ngram_deque()
    
    for line in inputfile:
        line = line.strip()
        if line:
            ngram.popleft()
            tag = line.split('\t')[3]
            ngram.append(tag)
            result[tuple(ngram)] += 1
        else:
            # end of sentence
            for i in range(args.N-1):
                ngram.popleft()
                ngram.append(END)
                result[tuple(ngram)] += 1

    inputfile.close()
    return result

def kl2invkl4(kl):
    return kl**-4


# MAIN

# the source language which we use to train the parser (Q)
source_counts = readfile(args.srcfile)
source_sum = sum(source_counts.values())

# the language we want to parse (P)
target_counts = readfile(args.tgtfile)
target_sum = sum(target_counts.values())

# smoothing
for ngram in target_counts:
    if not ngram in source_counts:
        source_counts[ngram] = SMOOTH
        source_sum += SMOOTH

dkl = 0

for ngram in target_counts:
    target_prob = target_counts[ngram]/target_sum 
    source_prob = source_counts[ngram]/source_sum 
    dkl += target_prob * log(target_prob/source_prob)

if args.inverse:
    print(kl2invkl4(dkl))
else:
    print(dkl)

