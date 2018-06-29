#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/th.tok.udpipe > th.tok

cat th.tok | tools/udpipe --tag --parse models/vi.trans_emb.th.udpipe > th.vi
cat th.tok | tools/udpipe --tag --parse models/id.trans_emb.th.udpipe > th.id
cat th.tok | tools/udpipe --tag --parse models/zh.trans_emb.th.udpipe > th.zh

# weights based on wals sim
# tree and deprel
tools/treecomb.sh th.vi th.id th.zh 75 64 60 > th.1
# lemma
tools/labelcomb_weighted.py 3 th.1 th.id th.zh 75 64 60 > th.2
# POS
tools/labelcomb_weighted.py 4 th.2 th.id th.zh 75 64 60 > th.3
# feats
tools/labelcomb_weighted.py 6 th.3 th.id th.zh 75 64 60 > th.4

cat th.4

