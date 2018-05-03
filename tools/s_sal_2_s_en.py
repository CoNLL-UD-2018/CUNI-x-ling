#!/usr/bin/env python3
#coding: utf-8

import sys

TGT_SIZE=149604

sentencesf = sys.argv[1]
alignmentf = sys.argv[2]

with open(sentencesf) as fh:
    sentences = fh.readlines()

tgt2src = dict()
with open(alignmentf) as fh:
    for line in fh:
        srcline, tgtline, _= line.split()
        tgt2src[int(tgtline)] = int(srcline)

for tgtline in range(TGT_SIZE):
    if tgtline in tgt2src:
        print(sentences[tgt2src[tgtline]], end='')
    else:
        print()

