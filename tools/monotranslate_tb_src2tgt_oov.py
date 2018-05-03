#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate
import words2freqlist

srcf = words2freqlist.Freqlist()
with open(sys.argv[1], "r") as srctb:
    for line in srctb:
        srcf.addtbline(line)

tgtf = words2freqlist.Freqlist()
with open(sys.argv[2], "r") as tgttb:
    for line in tgttb:
        tgtf.addtbline(line)

monotranslate.DEBUG = 0
monotranslate.OOV = 1
monotranslate.srclist = srcf.freqlist
monotranslate.tgtlist = tgtf.freqlist

sumscore = 0
countlines = 0
with open(sys.argv[1], "r") as srctb:
    for line in srctb:
        (translation, score, count) = monotranslate.translatetbline(line)
        sumscore += score
        countlines += count
        print(translation)
print("avgscore: " + str(sumscore/countlines), file=sys.stderr)
