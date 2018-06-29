#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize --tag models/hy.sup.udpipe  > hy.tag

cat hy.tag | tools/udpipe --parse models/hy.emb.udpipe > hy.hy
cat hy.tag | tools/udpipe --parse models/lv.delex.udpipe > hy.lv
cat hy.tag | tools/udpipe --parse models/et.delex.udpipe > hy.et

# weights based on delex LAS
tools/treecomb.sh hy.hy hy.lv hy.et 57 56 51 | \
    tools/fix_morphology_by_unimorph.py morpho/hy

