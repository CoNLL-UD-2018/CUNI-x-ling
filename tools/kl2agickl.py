#!/usr/bin/env python3
#coding: utf-8

import sys
import math

def kl2agickl(kl):
    return math.exp(5/kl)

for line in sys.stdin:
    lang, kl = line.split()
    print(lang, kl2agickl(float(kl)), sep="\t")


