#!/bin/bash

# TODO cobmine with delex tr, ug, kk? ale ony ty tagy budou hodně blbě už tak takže to asi moc nepomůže...

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/bxr_bdt.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag models/bxr.devow.udpipe \
    > bxr.tag

cat bxr.tag | tools/udpipe --parse models/bxr.devow.udpipe > bxr.bxr
cat bxr.tag | tools/udpipe --parse models/hi.delex.udpipe > bxr.hi
cat bxr.tag | tools/udpipe --parse models/ug.delex.udpipe > bxr.ug

# weights based on delex LAS
tools/treecomb.sh bxr.bxr bxr.hi bxr.ug 45 41 38 | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l

