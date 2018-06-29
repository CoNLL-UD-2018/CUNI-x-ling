#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/no.sup.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    tools/udpipe --tag --parse models/no.devow.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l | \
    tools/fix_morphology_by_unimorph.py morpho/fo

