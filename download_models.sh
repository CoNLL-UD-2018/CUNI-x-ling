#!/bin/bash

mkdir -p models
cd models

url=$(cat ../ufallab.url)/models/
for f in $(cat ../models.list)
do
    wget ${url}${f}
done



# default models for the langs (for cross-lingual stuff
# and for test treebanks without training data)
# e.g. cs.sup.udpipe -> cs_pdt.sup.udpipe

for d in $(cat ../defaults.list)
do
    for f in $d.*
    do
        ln -s $f $(echo $f | sed 's/_[a-z]*//')
    done
done

