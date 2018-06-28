#!/usr/bin/env python3
#coding: utf-8

import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        fields[1] = fields[2]
        print(*fields, sep='\t')
    else:
        print(line)

