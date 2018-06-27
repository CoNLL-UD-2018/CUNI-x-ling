#!/usr/bin/env python3
#coding: utf-8

import json
import sys
import os.path

# raw input text:
#   language['rawfile']
# segmented, tokenized and morphotagged data (with baseline models):
#   language['psegmorfile']


inputDataset, outputDir = sys.argv[1:]

def sup(lcode, tcode=None):
    if (tcode is not None):
        return 'CUNI-x-ling/models/' + lcode + '_' + tcode + '.sup.udpipe'
    else:
        return 'CUNI-x-ling/models/' + lcode + '.sup.udpipe'

def run(lcode):
    return 'CUNI-x-ling/run/' + lcode + '.sh'

udpipe = './udpipe --tokenize --tag --parse '

with open(inputDataset+'/metadata.json', 'r') as metadata:
    data = json.load(metadata)
    for language in data:

        # cat the input file
        catinput  = 'cat ' + inputDataset + '/' + language['rawfile'] + ' |' 

        # run udpipe
        if os.path.isfile(run(language['lcode'])):
            # for special targets, there is a file with the commands to run
            runudpipe = run(language['lcode'])
        elif os.path.isfile( sup(language['lcode'], language['tcode']) ):
            # for most targets, there is the lcode_tcode model
            runudpipe = udpipe + sup(language['lcode'], language['tcode'])
        else:
            # if not, use the default model for the lcode
            runudpipe = udpipe + sup(language['lcode'])

        # save the output
        diroutput = '> ' + outputDir + '/' + language['outfile']

        print(catinput, runudpipe, diroutput)


