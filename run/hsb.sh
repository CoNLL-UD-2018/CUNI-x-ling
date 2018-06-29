#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize --tag models/hsb.sup.udpipe > hsb.tag

# TODO emb
cat hsb.tag | tools/udpipe --parse models/hsb.emb.udpipe > hsb.hsb
cat hsb.tag | tools/udpipe --parse models/cs.delex.udpipe > hsb.cs
cat hsb.tag | tools/udpipe --parse models/hr.delex.udpipe > hsb.hr
cat hsb.tag | tools/udpipe --parse models/ru.delex.udpipe > hsb.ru
cat hsb.tag | tools/udpipe --parse models/sk.delex.udpipe > hsb.sk
cat hsb.tag | tools/udpipe --parse models/sl.delex.udpipe > hsb.sl

# weights based on delex LAS
tools/treecomb.sh hsb.hsb hsb.cs hsb.hr hsb.ru hsb.sk hsb.sl 53 73 70 66 69 68 | \
    tools/fix_morphology_by_unimorph.py morpho/hsb


