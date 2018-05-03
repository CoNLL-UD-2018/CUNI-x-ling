#!/usr/bin/env python3
#coding: utf-8

import sys
from collections import defaultdict, Counter
import math

# 0
# 1: 1x tgt text
#    Nx src parse: sequence of parent ords
#    Nx src-tgt alignment
#  +-Nx src weight

# parameters
tgt_f = sys.argv[1]
arg_groups = 3 if sys.argv[0].endswith('weighted.py') else 2
N = (len(sys.argv)-2)/arg_groups
assert N == int(N), "must have matching number of arguments"
N = int(N)
src_parse_f = sys.argv[2:N+2]
alignment_f = sys.argv[N+2:2*N+2]
if arg_groups == 2:
    src_weights = [1] * N
else:
    src_weights = [float(w) for w in sys.argv[2*N+2:]]

#            if alignment.count('\t'):
#                # last two elements are forward and backward alignment score
#                al_score *= math.exp(
#                        float(alignments.pop()) +
#                        float(alignments.pop()))
# return src-to-tgt dict
def align2dict(align):
    d = defaultdict(list)
    for st in align.split():
        (src, tgt) = st.split('-')
        # alignment is 0-based but ords are 1-based
        src = int(src)+1
        tgt = int(tgt)+1
        d[src].append(tgt)
    # root is always aligned to root
    d[0] = [0]
    return d

sent_len = list()
# sent_pc_weight[sent_id][child_id][parent_id] = score
# includes index 0, this is to be skipped (children 1-based)
sent_pc_weight = list()
with open(tgt_f) as tgt_fh:
    for line in tgt_fh:
        slen = len(line.split())
        sent_len.append(slen)
        sent_pc_weight.append([defaultdict(int) for child in range(slen+1)])
SENTS = len(sent_len)

for src in range(N):
    with open(alignment_f[src]) as alignment_fh, open(
            src_parse_f[src]) as src_parse_fh:
        sent = -1
        for line, alignment in zip(src_parse_fh, alignment_fh):
            sent += 1
            src2tgt = align2dict(alignment)
            parents = [int(p) for p in line.split()]
            children = range(1, len(parents)+1)
            for parent, child in zip(parents, children):
                for tgt_parent in src2tgt[parent]:
                    for tgt_child in src2tgt[child]:
                        sent_pc_weight[sent][tgt_child][tgt_parent] += src_weights[src]
            

for sent in range(SENTS):
    slen = sent_len[sent]
    print(slen, end=' ')
    for child in range(1, slen+1):
        # add root
        sent_pc_weight[sent][child][0] += 0
        # logits
        for parent in sent_pc_weight[sent][child]:
            sent_pc_weight[sent][child][parent] = math.exp(sent_pc_weight[sent][child][parent])
        # normalize and invert (because MST is Minimum spanning tree)
        Z = sum(sent_pc_weight[sent][child].values())
        for parent in sent_pc_weight[sent][child]:
            sent_pc_weight[sent][child][parent] /= -Z
            print(parent, child, sent_pc_weight[sent][child][parent], end=' ')
    print()


