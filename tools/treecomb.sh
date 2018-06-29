#!/bin/bash

# Usage: model model model weight weight weight
# e.g. with delex LAS as weight:
# - use parsers bxr.sup.udpipe hi.delex.udpipe ug.delex.udpipe
# to produce files bxr.bxr.sup bxr.hi.delex bxr.ug.delex
# - run this script with the parameters:
# bxr.bxr.sup bxr.hi.delex bxr.ug.delex 45 41 38

# $@ = all the púarsed files and then their weoights
# $1 = the first parsed file (use as base for output)

tools/treecomb_1_weighted.py $@ | \
    tools/chu_liu_edmonds.pl | \
    tools/treecomb_2.py $1 \
    > $1.combined

# combine deprels by voting
# instead of first file, the output of previous step will be used
shift
tools/labelcomb_weighted.py 8 $1.combined $@
rm $1.combined

