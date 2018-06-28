#!/bin/bash

mkdir -p models
cd models

url=$(cat ../ufallab.url)/models/
for f in $@
do
    wget ${url}${f}
done



# default models for the langs (for cross-lingual stuff
# and for test treebanks without training data)
# e.g. cs.sup.udpipe -> cs_pdt.sup.udpipe

for f in $@
do
    ln -s $f $(echo $f | sed 's/_[a-z]*//')
done

