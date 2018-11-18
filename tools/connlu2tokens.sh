#!/bin/bash

grep -v '^#' | grep -v '^[0-9]*[-.]' | \
    cut -f2 | sed 's/ /_/g' | \
    sed  's/^$/\t/' | tr "\n" " " | tr "\t" "\n" | sed -e 's/^ //' -e 's/ $//'

