#!/usr/bin/env python3
#coding: utf-8

import sys

lineno = 0
for line in sys.stdin:
    if lineno %3 == 1:
        print("aligning sent " + str(lineno//3), file=sys.stderr)
        parts = line.split('  # ')
        print(" ".join([str(s)+"-"+str(int(t)-1)
            for s,t in enumerate(parts[1].split(' '))
            if t != '0']))
    lineno += 1

