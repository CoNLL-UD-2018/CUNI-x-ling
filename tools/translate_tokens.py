#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle

# TRANSLATE TOKENIZED LOWERCASED TEXT, 1 sentence per line

print("Read in ttable", file=sys.stderr)
translation_table = pickle.load( open( sys.argv[1], "rb" ) )

print("Translate", file=sys.stderr)
found = 0
unfound = 0
def translate(word):
    global found, unfound
    translation = translation_table.get((word,), None)
    if translation:
        found += 1
    else:
        print('\t'.join(["OOV", word]), file=sys.stderr)
        translation = word
        unfound += 1
    return translation
    
for line in sys.stdin:
    line = line.rstrip('\n')
    tokens = line.split(' ')
    trans = [translate(token) for token in tokens]
    print(' '.join(trans))

print("found:", found, file=sys.stderr)
print("unfound:", unfound, file=sys.stderr)
print("OOV rate:", (100*unfound/(found+unfound)),"%" , file=sys.stderr)

