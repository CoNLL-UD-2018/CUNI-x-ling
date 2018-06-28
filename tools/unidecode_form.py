#!/usr/bin/env python3
#coding: utf-8

import sys
from unidecode import unidecode

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        fields[1] = unidecode(fields[1])
        print(*fields, sep='\t')
    else:
        print(line)

