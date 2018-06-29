#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/kmr.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag models/kmr.devow.udpipe \
    > kmr.tag

cat kmr.tag | tools/udpipe --parse models/kmr.devow.udpipe > kmr.kmr
cat kmr.tag | tools/udpipe --parse models/la_ittb.delex.udpipe > kmr.la
cat kmr.tag | tools/udpipe --parse models/el.delex.udpipe > kmr.el

# weights based on delex LAS
tools/treecomb.sh kmr.kmr kmr.la kmr.el 52 47 45 | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l

