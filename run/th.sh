#!/bin/bash

# TODO translate vi+zh+id->th, train standard udpipe
# beware: only id has reasonable tokenization
./udpipe --tokenize --tag --parse CUNI-x-ling/models/vi.sup.udpipe

