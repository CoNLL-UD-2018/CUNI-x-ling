#!/bin/bash

# TODO translate vi+zh+id->th, train standard udpipe
# beware: only id has reasonable tokenization
./udpipe --tokenize CUNI-x-ling/models/th.tok.udpipe | \
    ./udpipe --tag --parse CUNI-x-ling/models/id.sup.udpipe

# unidecode | \
