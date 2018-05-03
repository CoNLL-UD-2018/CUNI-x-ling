#!/usr/bin/env python3
#coding: utf-8

from math import log
import sys
import csv

# compute D_KL(P||Q)
# i.e. we approximate P by Q
# projection from lang1 to lang2

# read counts from files
def readfile(filename):
    result = dict()
    fh = open(filename)
    tsv = csv.reader(fh, delimiter='\t')
    for line in tsv:
        result[tuple(line[1:])] = int(line[0])
    return result

# the source language which we use to train the parser (Q)
source_counts = readfile(sys.argv[1])
source_sum = sum(source_counts.values())

# the language we want to parse (P)
target_counts = readfile(sys.argv[2])
target_sum = sum(target_counts.values())

# smoothing
for bigram in target_counts:
    if not bigram in source_counts:
        source_counts[bigram] = 1
        source_sum += 1

# added this now:
for bigram in source_counts:
    if not bigram in target_counts:
        target_counts[bigram] = 1
        target_sum += 1

dkl = 0

for bigram in target_counts:
    target_prob = target_counts[bigram]/target_sum 
    source_prob = source_counts[bigram]/source_sum 
    dkl += target_prob * log(target_prob/source_prob)

print(dkl)

