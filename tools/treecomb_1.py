#!/usr/bin/env python3

import sys
from collections import defaultdict

# TODO: now unlabelled, implement labelled

# TODO also projection

# inputs
arg_groups = 2 if sys.argv[0].endswith('weighted.py') else 1
N = (len(sys.argv)-1)/arg_groups
assert int(N) == N
N = int(N)
inputs = list()
for f in sys.argv[1:N+1]:
    inputs.append(open(f))
if arg_groups == 1:
    weights = [1] * N
else:
    weights = [float(w) for w in sys.argv[N+1:2*N+1]]

sent_len = dict()
sent_pc_weight = defaultdict(lambda: defaultdict(int))
for i in range(len(inputs)):
    fh = inputs[i]
    sent = 0
    maxord = 0
    for line in fh:
        line = line.strip()
        if line.startswith('#'):
            # comment
            pass
        elif not line:
            # end of sentence
            sent_len[sent] = maxord
            sent += 1
            maxord = 0
        else:
            fields = line.split('\t')
            parent = fields[6]
            child = fields[0]
            # - because MST computes MINIMUM spanning tree
            sent_pc_weight[sent][(parent, child)] -= weights[i]
            maxord = child


for sent in sent_pc_weight:
    # choose root
    root_children = [child for (parent, child) in sent_pc_weight[sent] if parent == 0]
    assert len(root_children) > 0
    if len(root_children) > 1:
        best_child = root_children[0]
        best_score = sent_pc_weight[sent][(0, best_child)]
        for child in root_children[1:]:
            score = sent_pc_weight[sent][(0, child)]
            if score < best_score:
                del sent_pc_weight[sent][(0, best_child)]
                best_child = child
                best_score = score
            else:
                del sent_pc_weight[sent][(0, child)]

    # output
    print (sent_len[sent], *[" ".join([
        parent,
        child,
        str(sent_pc_weight[sent][(parent, child)])
        ])
            for (parent, child) in sent_pc_weight[sent]])

for fh in inputs:
    fh.close()
