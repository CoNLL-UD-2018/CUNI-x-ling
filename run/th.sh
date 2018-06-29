#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/th.tok.udpipe > th.tok

cat th.tok | tools/udpipe --tag --parse models/id.trans_emb.th.udpipe > th.id
cat th.tok | tools/udpipe --tag --parse models/zh.trans_emb.th.udpipe > th.zh
cat th.tok | tools/udpipe --tag --parse models/vi.trans_emb.th.udpipe > th.vi

# weights based on mono LAS
# tree and deprel
tools/treecomb.sh th.id th.zh th.vi 75 55 40 > th.1
# lemma
tools/labelcomb_weighted.py 3 th.1 th.zh th.vi 75 55 40 > th.2
# POS
tools/labelcomb_weighted.py 4 th.2 th.zh th.vi 75 55 40 > th.3
# feats
tools/labelcomb_weighted.py 6 th.3 th.zh th.vi 75 55 40 > th.4

cat th.4

