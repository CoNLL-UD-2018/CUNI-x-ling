#!/bin/bash

if [ -z $3 ]
then
    echo "Usage: $0 setupname srclang tgtlang"
    echo
    echo "Known setup names: "
    cd templates;
    ls allsteps*|cut -d. -f1|tr "\n" " "
    echo
    echo
    echo "Known languages: "
    cd ../treebanks
    ls|cut -c1-2|sort -u|tr "\n" " "
    echo
else
    s=$1
    S=$2
    T=$3
    mkdir -p run
    sed -e s/SSS/$S/ -e s/TTT/$T/ templates/header-SSS-TTT.shc > run/$s-$S-$T.shc
    cat templates/$s.shc >> run/$s-$S-$T.shc
    echo Created run script: run/$s-$S-$T.shc >&2
    echo -e "To submit it, simply use:\n\ncd run; qsub $s-$S-$T.shc; cd ..\n" >&2

fi

