#!/bin/bash

#set -o xtrace

s=$1
t=$2

mkdir -p para
cd para

if wget http://opus.nlpl.eu/download/OpenSubtitles2018/$s-$t.txt.zip
then
    set -e
    unzip $s-$t.txt.zip
    ln -s OpenSubtitles2018.$s-$t.$s OpenSubtitles2018.$t-$s.$s
    ln -s OpenSubtitles2018.$s-$t.$t OpenSubtitles2018.$t-$s.$t
    rm $s-$t.txt.zip OpenSubtitles2018.$s-$t.ids
    echo Para data downloaded successfully! >&2
    exit 0
elif wget http://opus.nlpl.eu/download/OpenSubtitles2018/$t-$s.txt.zip
then
    set -e
    unzip $t-$s.txt.zip
    ln -s OpenSubtitles2018.$t-$s.$s OpenSubtitles2018.$s-$t.$s
    ln -s OpenSubtitles2018.$t-$s.$t OpenSubtitles2018.$s-$t.$t
    rm $t-$s.txt.zip OpenSubtitles2018.$t-$s.ids
    echo Para data downloaded successfully! >&2
    exit 0
else
    echo No para data found! >&2
    exit 1
fi

