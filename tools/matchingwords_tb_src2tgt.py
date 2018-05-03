#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate
import words2freqlist_simple
import math

srcf = words2freqlist_simple.Freqlist()
with open(sys.argv[1], "r") as srctb:
    for line in srctb:
        srcf.addtbline(line)

tgtf = words2freqlist_simple.Freqlist()
with open(sys.argv[2], "r") as tgttb:
    for line in tgttb:
        tgtf.addtbline(line)

# count proportion of tgt word types found in src
count_types = 0
match_types = 0
count_words = 0
match_words = 0

for word in tgtf.freqlist:
    count_types += 1
    count_words += tgtf.freqlist[word]
    if word in srcf.freqlist:
        match_types += 1
        match_words += srcf.freqlist[word]

print("matching types: " + str(match_types/count_types))
print("matching words: " + str(match_words/count_words))

