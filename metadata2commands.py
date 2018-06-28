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

# selectively running only for some languages
# languages = None
languages = set()
languages.add('pcm')
languages.add('th')
languages.add('fo')
languages.add('br')
languages.add('bxr')

# print(languages)

def sup(lcode, tcode=None):
    if (tcode is not None):
        return 'CUNI-x-ling/models/' + lcode + '_' + tcode + '.sup.udpipe'
    else:
        return 'CUNI-x-ling/models/' + lcode + '.sup.udpipe'

def run(lcode):
    return 'CUNI-x-ling/run/' + lcode + '.sh'

# udpipe_full = './udpipe --tokenize --tag --parse '
udpipe_parse = './udpipe --parse '

with open(inputDataset+'/metadata.json', 'r') as metadata:
    data = json.load(metadata)
    for language in data:

        # selectively running only for some languages
        if languages is not None and language['lcode'] not in languages:
            continue

        # Run udpipe
        if os.path.isfile(run(language['lcode'])):
            # For special targets, there is a file with the commands to run
            # In such case, we process the raw data
            catinput  = 'cat ' + inputDataset + '/' + language['rawfile'] + ' |' 
            runudpipe = run(language['lcode'])
        elif os.path.isfile( sup(language['lcode'], language['tcode']) ):
            # For most targets, there is the lcode_tcode model
            # We do only parsing
            catinput  = 'cat ' + inputDataset + '/' + language['psegmorfile'] + ' |' 
            runudpipe = udpipe_parse + sup(language['lcode'], language['tcode'])
        else:
            # If not, use the default model for the lcode
            # We do only parsing
            catinput  = 'cat ' + inputDataset + '/' + language['psegmorfile'] + ' |' 
            runudpipe = udpipe_parse + sup(language['lcode'])

        # save the output
        diroutput = '> ' + outputDir + '/' + language['outfile']

        print(catinput, runudpipe, diroutput)


