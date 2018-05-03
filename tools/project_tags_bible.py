#!/usr/bin/env python3
#coding: utf-8

# projects tags or deprels

import sys
from collections import defaultdict, Counter
import math

DEFAULT_TAG = 'NOUN'

# 0
# 1: 1x tgt text
#    Nx src UPOS
#    Nx src-tgt alignment
#  +-Nx src weight

# parameters
tgt_f = sys.argv[1]
arg_groups = 3 if sys.argv[0].endswith('weighted.py') else 2
N = (len(sys.argv)-2)/arg_groups
assert N == int(N), "must have matching number of arguments"
N = int(N)
src_pos_f = sys.argv[2:N+2]
alignment_f = sys.argv[N+2:2*N+2]
src_weights = [float(w) for w in sys.argv[2*N+2:]]  # empty if arg_groups=2

# open files
tgt_fh = open(tgt_f)
src_pos_fh = [open(filename) for filename in src_pos_f]
alignment_fh = [open(filename) for filename in alignment_f]

words = list()
tags = list()
word_tags = defaultdict(Counter)
all_tags = Counter()
for line in tgt_fh:
    words.append(line.split())
    length = len(words[-1])
    tags.append([Counter() for _ in range(length)])
    for src in range(N):
        src_pos = src_pos_fh[src].readline()
        alignment = alignment_fh[src].readline()
        if alignment == '\n':
            # this tgt line has no counterpart in this src
            continue
        else:
            assert src_pos != '\n', "all aligned lines must have POS tags"
            src_pos = src_pos.split()
            alignments = alignment.split()
            al_score = 1
            if src_weights:
                al_score = src_weights[src]
            if alignment.count('\t'):
                # last two elements are forward and backward alignment score
                al_score *= math.exp(
                        float(alignments.pop()) +
                        float(alignments.pop()))
            for link in alignments:
                i_src, i_tgt = [int(i) for i in link.split('-')]
                pos = src_pos[i_src]
                tags[-1][i_tgt][pos] += al_score
                word_tags[words[-1][i_tgt]][pos] += al_score
                all_tags[pos] += al_score

DEFAULT_TAG = all_tags.most_common(1)[0][0]

for line in range(len(words)):
    line_words = words[line]
    line_tags = tags[line]
    result = []
    for i_tgt in range(len(line_words)):
        word = line_words[i_tgt]
        if line_tags[i_tgt]:
            result.append(line_tags[i_tgt].most_common(1)[0][0])
        elif word in word_tags:
            result.append(word_tags[word].most_common(1)[0][0])
        else:
            print("No tag for", word,
                    "using the default tag", DEFAULT_TAG,
                    file=sys.stderr)
            result.append(DEFAULT_TAG)
    print(*result)


# close files
tgt_fh.close()
for fh in src_pos_fh:
    fh.close()
for fh in alignment_fh:
    fh.close()

