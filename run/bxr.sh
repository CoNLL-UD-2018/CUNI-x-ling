#!/bin/bash

# TODO cobmine with delex tr, ug, kk? ale ony ty tagy budou hodně blbě už tak takže to asi moc nepomůže...

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/bxr_bdt.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag --parse models/bxr.devow.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l



