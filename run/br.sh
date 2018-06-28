#!/bin/bash

# TODO translate fr->br, train standard udpipe
# TODO: unimorph: fix tags and feats before parsing, and lemmas after lemma restore

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/fr.sup.udpipe | \
    tools/copy_form_to_col8.py -u | \
    tools/devow_form.py | \
    tools/udpipe --tag --parse models/fr.devow.udpipe | \
    tools/copy_col8_to_form.py -u | \
    tools/copy_form_to_lemma.py -l

