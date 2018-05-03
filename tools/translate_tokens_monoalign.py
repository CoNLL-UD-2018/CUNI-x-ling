#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle

# TRANSLATE TOKENIZED CLEANED TEXT, 1 sentence per line

print("Read in ttable", file=sys.stderr)
ttable = dict()
with open( sys.argv[1], "r" ) as ttable_f:
    for line in ttable_f:
        (srcword, tgtword, _) = line.split()
        ttable[srcword] = tgtword

print("Translate", file=sys.stderr)
found = 0
unfound = 0
def translate(word):
    global found, unfound
    translation = word
    if word in ttable:
        found += 1
        translation = ttable[word]
    elif word.lower() in ttable:
        found += 1
        translation = ttable[word.lower()]
    else:
        unfound += 1
        print('\t'.join(["OOV", word]), file=sys.stderr)
    return translation
    
for line in sys.stdin:
    line = line.rstrip('\n')
    tokens = line.split(' ')
    trans = [translate(token) for token in tokens]
    print(' '.join(trans))

print("found:", found, file=sys.stderr)
print("unfound:", unfound, file=sys.stderr)
print("OOV rate:", (100*unfound/(found+unfound)),"%" , file=sys.stderr)

