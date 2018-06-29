#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/kk.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag models/kk.devow.udpipe \
    > kk.tag

cat kk.tag | tools/udpipe --parse models/kk.devow.udpipe > kk.kk
cat kk.tag | tools/udpipe --parse models/tr.delex.udpipe > kk.tr
cat kk.tag | tools/udpipe --parse models/ug.delex.udpipe > kk.ug

# weights based on delex LAS
tools/treecomb.sh kk.kk kk.tr kk.ug 44 33 29 | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l | \
    tools/fix_morphology_by_unimorph.py morpho/kk

