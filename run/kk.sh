#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize --tag models/kk.sup.udpipe > kk.tag

cat kk.tag | tools/udpipe --parse models/kk.emb.udpipe > kk.kk
cat kk.tag | tools/udpipe --parse models/tr.delex.udpipe > kk.tr
cat kk.tag | tools/udpipe --parse models/ug.delex.udpipe > kk.ug

# weights based on delex LAS
tools/treecomb.sh kk.kk kk.tr kk.ug 44 33 29 | \
    tools/fix_morphology_by_unimorph.py morpho/kk

