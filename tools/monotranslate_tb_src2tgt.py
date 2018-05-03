#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate
import words2freqlist
import math

srcf = words2freqlist.Freqlist()
with open(sys.argv[1], "r") as srctb:
    for line in srctb:
        srcf.addtbline(line)

tgtf = words2freqlist.Freqlist()
with open(sys.argv[2], "r") as tgttb:
    for line in tgttb:
        tgtf.addtbline(line)

# downscale frequencies so that the distros are similar;
# in the smaller dataset, the distro is more peaked,
# so we increase the dataset size to make the distro flatter
src_count = srcf.freqlist[None][None]
tgt_count = tgtf.freqlist[None][None]

TRY_ALL_LIMIT = 10000
if tgt_count < TRY_ALL_LIMIT:
    monotranslate.TRY_ALL = 1

if src_count > tgt_count:
    tgtf.freqlist[None][None] = tgt_count * math.sqrt(src_count/tgt_count)
else:
    srcf.freqlist[None][None] = src_count * math.sqrt(tgt_count/src_count)

monotranslate.DEBUG = 0
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
