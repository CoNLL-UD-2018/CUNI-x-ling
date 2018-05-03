#!/bin/bash

if [ -z $1 ]
then
    col=2
else
    col=$1
fi

cut -f$col | sed 's/^$/\t/' | tr "\n" " " | tr "\t" "\n" | sed -e 's/^ //' -e 's/ $//'

