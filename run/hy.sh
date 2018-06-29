#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/hy.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag models/hy.devow.udpipe \
    > hy.tag

cat hy.tag | tools/udpipe --parse models/hy.devow.udpipe > hy.hy
cat hy.tag | tools/udpipe --parse models/lv.delex.udpipe > hy.lv
cat hy.tag | tools/udpipe --parse models/et.delex.udpipe > hy.et

# weights based on delex LAS
tools/treecomb.sh hy.hy hy.lv hy.et 57 56 51 | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l

