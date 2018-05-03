#!/usr/bin/env python3
#coding: utf-8

import sys
import words2freqlist_simple
import math
from collections import defaultdict

def tb2freq(tbfile):
    freqlist = Counter()
    with open(tbfile, "r") as tb:
        for line in tb:
            line = line.rstrip('\n')
            if line != '' and not line.startswith('#'):
                fields = line.split('\t')
                word = fields[1]
                for char in word:
                    freqlist[char] += 1

srcf = tb2freq(sys.argv[1])
srctotal = len(srcf.elements())
tgtf = tb2freq(sys.argv[2])
tgttotal = len(tgtf.elements())

kl = 0
for char in tgtf:
    tgt_freq = tgtf[char] / tgttotal
    if char in srcf:
        src_freq = srcf[char] / srctotal
    else:
        src_freq = 1 / srctotal        
    kl += tgt_freq * math.log(tgt_freq/src_freq)

print(kl)
