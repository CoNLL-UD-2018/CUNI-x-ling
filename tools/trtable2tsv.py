#!/usr/bin/env python3
#coding: utf-8

import sys
import pickle

name = sys.argv[1]

trtable = pickle.load(open(name, 'rb'))

for src in sorted(trtable.keys()):
    print(src, trtable[src], sep='\t')


