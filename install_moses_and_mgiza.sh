#!/bin/bash

# install moses
git clone https://github.com/moses-smt/mosesdecoder.git 
cd mosesdecoder
./compile.sh
cd ..

# install mgiza
git clone https://github.com/moses-smt/mgiza.git
cd mgiza/mgizapp
cmake .
make
make install
cd ../..

# symlink mgiza to moses tools
mkdir -p mosesdecoder/tools
cd mosesdecoder/tools
for f in ../../mgiza/mgizapp/bin/* ../../mgiza/mgizapp/scripts/merge_alignment.py
do
    ln -s $f
done
cd ../..

# moses to be used with the option
# -external-bin-dir mosesdecoder/tools

