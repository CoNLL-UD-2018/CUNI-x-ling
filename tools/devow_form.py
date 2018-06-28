#!/usr/bin/env python3
#coding: utf-8

import sys
from unidecode import unidecode

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        form = fields[1]
        
        form = unidecode(form)
        form = form.lower()
        form = form.replace("a", "")
        form = form.replace("e", "")
        form = form.replace("i", "")
        form = form.replace("o", "")
        form = form.replace("u", "")
        form = form.replace("y", "")
        if form == "":
            form = "_"
        
        fields[1] = form
        print(*fields, sep='\t')
    else:
        print(line)

