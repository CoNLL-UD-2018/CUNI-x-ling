#!/bin/bash

if [ -z $1 ]
then
    echo "Usage: $0 setupname"
    echo
    echo "Known setup names: "
    cd templates;
    ls allsteps*|cut -d. -f1|tr "\n" " "
    echo
    echo
    echo "Language pairs used: "
    cd ..
    cat LANG_PAIRS
    echo
else
    s=$1
    while read lp
    do
        eval ./new_shc_setup.sh $1 $lp
    done < LANG_PAIRS
fi

