#!/usr/bin/env python3

import sys
from unidecode import unidecode

for line in sys.stdin:
    line = line.rstrip('\n')
    if line != '' and not line.startswith('#'):
        fields = line.split('\t')
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
        print('\t'.join(fields))
    else:
        print(line)

