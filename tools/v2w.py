#!/usr/bin/env python3
#coding: utf-8

import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        form = fields[1]
        form = form.replace('v', 'w')
        if form.lower().startswith('o'):
            form = 'w' + form
        fields[1] = form
        print(*fields, sep='\t')
    else:
        print(line)

