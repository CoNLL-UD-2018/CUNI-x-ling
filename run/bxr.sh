#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/bxr.sup.udpipe | \
    tools/udpipe --tag models/bxr.sup.udpipe \
    > bxr.tag

cat bxr.tag | tools/udpipe --parse models/bxr.emb.udpipe > bxr.bxr
cat bxr.tag | tools/udpipe --parse models/hi.delex.udpipe > bxr.hi
cat bxr.tag | tools/udpipe --parse models/ug.delex.udpipe > bxr.ug

# weights based on delex LAS
tools/treecomb.sh bxr.bxr bxr.hi bxr.ug 45 41 38

