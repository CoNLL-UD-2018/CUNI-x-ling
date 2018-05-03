#!/usr/bin/env python3

import sys

FEAT = sys.argv[1]
for line in sys.stdin:
    line = line.rstrip('\n')
    if line != '' and not line.startswith('#'):
        fields = line.split('\t')
        feats = fields[5].split('|')
        fields[5] = '_'
        for feat in feats:
            if feat.startswith(FEAT):
                fields[5] = feat
        print('\t'.join(fields))
    else:
        print(line)

