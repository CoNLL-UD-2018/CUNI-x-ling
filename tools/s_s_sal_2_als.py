#!/usr/bin/env python3
#coding: utf-8

import sys

src_f = open(sys.argv[1])
src = src_f.readlines()
src_f.close()

tgt_f = open(sys.argv[2])
tgt = tgt_f.readlines()
tgt_f.close()

sal_f = open(sys.argv[3])
for line in sal_f:
    src_i, tgt_i, _ = line.split()
    src_snt = src[int(src_i)].strip()
    tgt_snt = tgt[int(tgt_i)].strip()
    print(src_snt + '\t' + tgt_snt)
sal_f.close()

