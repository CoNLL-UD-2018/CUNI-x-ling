#!/bin/bash

cd ~/CUNI-x-ling/

tools/udpipe --tokenize models/fr.sup.udpipe | \
    tools/udpipe --tag --parse models/fr.trans.br.udpipe | \
    tools/fix_morphology_by_unimorph.py morpho/br

