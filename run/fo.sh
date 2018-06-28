#!/bin/bash

# TODO: monotranslate input to nynorsk
# TODO: unimorph: fix tags and feats before parsing, and lemmas after lemma restore

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/no.sup.udpipe | \
    tools/copy_form_to_col8.py \
    > fo.tok

    # tools/words2freqlist_simple_tb.py fo.tok fo.freqlist
    # "TRANSLATE" FORM FROM PCM TO NO | \

cat fo.tok | \
    tools/devow_form.py | \
    tools/udpipe --tag --parse models/no.devow.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l

