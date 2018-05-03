#!/bin/bash

git clone https://github.com/clab/fast_align.git
cd fast_align
mkdir build
cd build
cmake ..
make

ln -s fast_align/build/fast_align fastalign
ln -s fast_align/build/atools

mkdir -p fastwork

