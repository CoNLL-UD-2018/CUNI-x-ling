#!/bin/bash

cd ~/CUNI-x-ling/

# tools/udpipe --tokenize --tag models/hsb.sup.udpipe > hsb.tag

#tools/udpipe --tokenize --tag models/pl.sup.udpipe |\
#    tools/fix_morphology_by_unimorph.py morpho/hsb \
#    > hsb.tag

tools/udpipe --tokenize models/pl.sup.udpipe > hsb.tok

cat hsb.tok | tools/udpipe --tag models/hsb.sup.udpipe > hsb.hsb
cat hsb.tok | tools/udpipe --tag models/pl.sup.udpipe > hsb.pl
cat hsb.tok | tools/udpipe --tag models/cs.monotrans.hsb.udpipe > hsb.csm
cat hsb.tok | tools/udpipe --tag models/cs.sup.udpipe > hsb.cs

# weights based on eval on hsb train
# lemma
tools/labelcomb_weighted.py 3 hsb.hsb hsb.pl hsb.cs 40 60 51 > hsb.1
# POS
tools/labelcomb_weighted.py 4 hsb.1 hsb.pl hsb.csm 100 69 65 > hsb.2
# feats
tools/labelcomb_weighted.py 6 hsb.2 hsb.pl hsb.csm 30 10 24 > hsb.3

cat hsb.3 | \
    tools/fix_morphology_by_unimorph.py morpho/hsb \
    > hsb.tag

cat hsb.tag | tools/udpipe --parse models/hsb.emb.udpipe > hsb.hsb
cat hsb.tag | tools/udpipe --parse models/cs.delex.udpipe > hsb.cs
cat hsb.tag | tools/udpipe --parse models/hr.delex.udpipe > hsb.hr
cat hsb.tag | tools/udpipe --parse models/ru.delex.udpipe > hsb.ru
cat hsb.tag | tools/udpipe --parse models/sk.delex.udpipe > hsb.sk
cat hsb.tag | tools/udpipe --parse models/sl.delex.udpipe > hsb.sl

# weights based on delex LAS
tools/treecomb.sh hsb.hsb hsb.cs hsb.hr hsb.ru hsb.sk hsb.sl 53 73 70 66 69 68


