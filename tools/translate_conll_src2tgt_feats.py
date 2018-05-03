#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle

print("Read in ttable", file=sys.stderr)
translation_table = pickle.load( open( sys.argv[1], "rb" ) )

print("Translate", file=sys.stderr)
found = 0
unfound = 0
def translate(word, tag, feats):
    global found, unfound
    lword = word.lower()
    keys = [(word,tag,feats), (lword,tag,feats),
            (word,tag), (lword,tag),
            (word,), (lword,)]
    translation = None
    for key in keys:
        translation = translation_table.get(key, None)
        if translation:
            # print(key, file=sys.stderr)
            break
    if not translation:
        # print('\t'.join(["OOV", tag, word, feats]), file=sys.stderr)
        translation = word
        unfound += 1
    else:
        found += 1
    return translation
    
for line in sys.stdin:
    line = line.rstrip('\n')
    if line != '' and not line.startswith('#'):
        fields = line.split('\t')
        fields[1] = translate(fields[1], fields[3], fields[5])
        print('\t'.join(fields))
    else:
        print(line)

print("found:", found, file=sys.stderr)
print("unfound:", unfound, file=sys.stderr)
print("OOV rate:", (100*unfound/(found+unfound)),"%" , file=sys.stderr)

