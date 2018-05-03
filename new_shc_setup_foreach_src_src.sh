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
    cat langs_src
    echo
else
    while read s
    do
        eval ./new_shc_setup.sh $1 $s $s
    done < langs_src
fi

