#!/usr/bin/env python3
#coding: utf-8

import json
import sys

inputDataset, outputDir = sys.argv[1:]

with open(inputDataset+'/metadata.json', 'r') as metadata:
    data = json.load(metadata)
    for language in data:
        model = 'udpipe-ud-2.0-170801/' + language['lcode'] + '_' + language['tcode'] + '.udpipe'

        # catinput  = 'cat ' + inputDataset + '/' + language['psegmorfile'] + ' |' 
        catinput  = 'cat ' + inputDataset + '/' + language['rawfile'] + ' |' 
        # runudpipe = './udpipe --tag --parse ' + model
        runudpipe = './udpipe --tokenize --tag --parse ' + model
        diroutput = '> ' + outputDir + '/' + language['outfile']

        print(catinput, runudpipe, diroutput)


