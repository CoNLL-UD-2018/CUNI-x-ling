#!/bin/bash

# TODO: monotranslate input to en (use en_wtb forms as vocabulary corpus?)

cd ~/CUNI-x-ling

tools/udpipe --tokenize models/en.sup.udpipe | \
    tools/copy_form_to_col8.py \
    > pcm.tok

    # tools/words2freqlist_simple_tb.py pcm.tok pcm.freqlist
    
cat pcm.tok | tools/translate_pcm_treebank.py en.dict | \
    tools/udpipe --tag --parse models/en.sup.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l -s

