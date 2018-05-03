#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.rstrip('\n')
    if line != '' and not line.startswith('#'):
        fields = line.split('\t')
        fields[7] = fields[7].split(':')[0]
        print('\t'.join(fields))
    else:
        print(line)

