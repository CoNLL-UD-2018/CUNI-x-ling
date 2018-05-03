#!/usr/bin/env python3
#coding: utf-8

# Usage: ./hun_merge_partialAlign.py batch > merged.align

import sys
import os.path

batchf = sys.argv[1]
basedir = os.path.dirname(batchf)

def f(filename):
    return os.path.join(basedir, filename)

def l(filename):
    with open(f(filename)) as fh:
        return len(fh.readlines())
    

src_add = 0
tgt_add = 0
with open(batchf) as batch:
    for batch_line in batch:
        (srcf, tgtf, alnf) = batch_line.split()
        try:
            with open(f(alnf)) as aln:
                for aln_line in aln:
                    (srcl, tgtl, score) = aln_line.split()
                    print(int(srcl)+src_add, int(tgtl)+tgt_add, score, sep='\t')
        except FileNotFoundError:
            print("WARN: skipping non-existent alignment file", f(alnf), file=sys.stderr)
        src_add += l(srcf)
        tgt_add += l(tgtf)

print("src lines:", src_add, "tgt lines:", tgt_add, file=sys.stderr)

