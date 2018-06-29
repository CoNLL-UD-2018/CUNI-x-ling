#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/en.sup.udpipe | \
    tools/copy_form_to_col8.py \
    tools/translate_pcm_treebank.py en.dict | \
    #tools/translate_pcm_treebank_wiki.py en.dict | \
    tools/udpipe --tag --parse models/en.sup.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l -s

