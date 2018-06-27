#!/bin/bash

# TODO: monotranslate input to no (??? bokmal vs nynorsk !!!), process, by no udpipe model, then restore the original word forms
# ? probably should tokenize as is (to get the "forms" column), the tag and parse, and then restore the forms (and use lemma=form)

./udpipe --tokenize CUNI-x-ling/models/no.sup.udpipe
    COPY FORM TO LEMMA | \
    "TRANSLATE" FORM FROM PCM TO NO | \

    ./udpipe --tag CUNI-x-ling/models/no.tag-nolemma.udpipe
    
    FIX TAGS AND FEATS BASED ON UniMorph; keep lemma, this will be used as the form in the output!

    ./udpipe --parse CUNI-x-ling/models/no.sup.udpipe

    COPY LEMMA TO FORM

    FIX LEMMAS BASED ON UniMorph

