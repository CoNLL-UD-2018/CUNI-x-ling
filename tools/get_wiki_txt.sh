#!/bin/bash

l=$1
mkdir -p data
wget https://dumps.wikimedia.org/${l}wiki/latest/${l}wiki-latest-pages-articles-multistream.xml.bz2 -O data/$l.xml.bz2
cd data
bunzip2 $l.xml.bz2
cd ..
wikiextractor/WikiExtractor.py --txt data/$l.xml -o - | sed 's/<[^>]*>//g' | gzip > data/$l.txt.gz
rm data/$l.xml

