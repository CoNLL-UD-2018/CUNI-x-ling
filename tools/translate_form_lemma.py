#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle

print("Read in ttable", file=sys.stderr)
translation_table = pickle.load( open( sys.argv[1], "rb" ) )

found = 0
unfound = 0

print("Translate", file=sys.stderr)
def translate(word):
    global found, unfound
    if word in translation_table:
        found += 1
        return translation_table[word]
    elif word.lower() in translation_table:
        found += 1
        return translation_table[word.lower()]
    else:
        unfound += 1
        return word

with open(sys.argv[2], 'r') as data:
    for line in data:
        line = line.rstrip('\n')
        fields = line.split('\t')
        if fields[0].isdigit():
            fields[1] = translate(fields[1])
            fields[2] = translate(fields[2])
            print(*fields, sep='\t')
        else:
            print(line)

print("found:", found, file=sys.stderr)
print("unfound:", unfound, file=sys.stderr)
print("unfound rate:", (100*unfound/(found+unfound)),"%" , file=sys.stderr)

