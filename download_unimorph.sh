#!/bin/bash

mkdir morpho
cd morpho

git clone git@github.com:sigmorphon/conll2018.git

D=conll2018/task1/all

ln -s $D/armenian-train-high           hy
ln -s $D/breton-train-high             br
ln -s $D/faroese-train-high            fo
ln -s $D/kazakh-train-medium           kk
ln -s $D/kurmanji-train-high           kmr
ln -s $D/lower-sorbian-train-high      hsb

# hoping hsb and lsb are sufficiently similar

