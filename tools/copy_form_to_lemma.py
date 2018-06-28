#!/usr/bin/env python3
#coding: utf-8

import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--strips", help="strip trailing -s from lemma",
        action="store_true")
parser.add_argument("-l", "--lowercase", help="lowercase the lemmma",
        action="store_true")
args = parser.parse_args()

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        lemma = fields[1]
        if args.strips and len(lemma) > 3:
            if lemma.endswith('s') or lemma.endswith('S'):
                lemma = lemma[:-1]
        if args.lowercase:
            lemma = lemma.lower()
        fields[2] = lemma
        print(*fields, sep='\t')
    else:
        print(line)

