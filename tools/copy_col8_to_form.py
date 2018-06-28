#!/usr/bin/env python3
#coding: utf-8

import sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--underscores", help="convert space to underscore",
        action="store_true")
args = parser.parse_args()


for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        form = fields[8]
        if args.underscores:
            form = form.replace("_", " ")
            form = form.replace("    ", "_")
        fields[1] = form
        fields[8] = '_'
        print(*fields, sep='\t')
    else:
        print(line)

