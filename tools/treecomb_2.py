#!/usr/bin/env python3

import sys
from collections import defaultdict

# return child-to-parent dict
def mst2dict(mst):
    d = dict()
    for pc in mst.split():
        (parent, child) = pc.split('-')
        d[child] = parent
    return d

with open(sys.argv[1]) as conllu:
    parent = mst2dict(sys.stdin.readline())
    for line in conllu:
        line = line.strip()
        if line.startswith('#'):
            # comment
            pass
        elif not line:
            # end of sentence
            print()
            # new tree for next sentence
            parent = mst2dict(sys.stdin.readline())
        else:
            fields = line.split('\t')
            child = fields[0]
            fields[6] = parent[child]
            print(*fields, sep='\t')

