#!/bin/bash

# TODO translate TH to VI, ID, ZH; tag and parse; combine

cd ~/CUNI-x-ling/

./udpipe --tokenize models/th.tok.udpipe | \
    tools/copy_form_to_col8.py | \
    tools/devow_form.py | \
    ./udpipe --tag --parse models/vi.devow.udpipe | \
    tools/copy_col8_to_form.py | \
    tools/copy_form_to_lemma.py -l

