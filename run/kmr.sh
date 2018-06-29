#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize --tag models/kmr.sup.udpipe > kmr.tag

# TODO emb
cat kmr.tag | tools/udpipe --parse models/kmr.sup.udpipe > kmr.kmr
cat kmr.tag | tools/udpipe --parse models/la_ittb.delex.udpipe > kmr.la
cat kmr.tag | tools/udpipe --parse models/el.delex.udpipe > kmr.el

# weights based on delex LAS
tools/treecomb.sh kmr.kmr kmr.la kmr.el 52 47 45 | \
    tools/fix_morphology_by_unimorph.py morpho/kmr

