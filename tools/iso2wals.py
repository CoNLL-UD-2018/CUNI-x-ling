#!/usr/bin/env python3
#coding: utf-8

import sys

iso2wals = dict()
with open('langs_wals') as langs_wals:
    for line in langs_wals:
        iso, wals = line.split()
        iso2wals[iso] = wals

print(iso2wals[sys.argv[1]])

