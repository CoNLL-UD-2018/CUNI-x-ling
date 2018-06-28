#!/bin/bash

# TODO: monotranslate input to en (use en_wtb forms as vocabulary corpus?), process, by en udpipe model, then restore the original word forms
# ? probably should tokenize as is (to get the "forms" column), the tag and parse, and then restore the forms (and use lemma=form)

./udpipe --tokenize CUNI-x-ling/models/en.sup.udpipe | \
    tools/copy_form_to_lemma.py | \
    > pcm.tok

    tools/words2freqlist_simple_tb.py pcm.tok pcm.freqlist
    
    cat pcm.tok | tools/translate_pcm_treebank.py en.dict | \
    tools/udpipe --tag CUNI-x-ling/models/en.tag-nolemma.udpipe | \
    tools/udpipe --parse CUNI-x-ling/models/en.sup.udpipe | \
    tools/compy_lemma_to_form.py
# TODO: CUT -s FROM LEMMA

