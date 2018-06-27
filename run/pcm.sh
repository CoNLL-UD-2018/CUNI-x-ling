#!/bin/bash

# TODO: monotranslate input to en (use en_wtb forms as vocabulary corpus?), process, by en udpipe model, then restore the original word forms
# ? probably should tokenize as is (to get the "forms" column), the tag and parse, and then restore the forms (and use lemma=form)
./udpipe --tokenize --tag --parse CUNI-x-ling/models/en.sup.udpipe

