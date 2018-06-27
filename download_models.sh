#!/bin/bash

mkdir -p models
cd models

url=$(cat ../ufallab.url)
for f in $(cat ../models.list)
do
    wget ${url}${f}
done

