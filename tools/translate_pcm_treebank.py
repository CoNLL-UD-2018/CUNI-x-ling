#!/usr/bin/env python3
#coding: utf-8

import sys
import re

lexicon = {'sey'  : 'that',
           'na'   : 'is',
           'wey'  : 'which',
           'im'   : 'his',
           'wetin': 'what',
           'dey'  : 'is',
           'e'    : 'he',
           'dem'  : 'they',
           'dis'  : 'this',
           'de'   : 'is',
           'don'  : 'has',
           'am'   : 'him',
           'go'   : 'will',
           'no'   : 'not',
           'di'   : 'the',
           }

rules = [('i', 'y'), ('d', 'th'), ('t', 'th'), ('a$', 'er'), ('k', 'c'), ('^', 'h'), ('$', 't')]

en_words = dict()

with open(sys.argv[1], 'r') as en_dict:
    for word in en_dict:
        word = word.strip()
        en_words[word] = 1

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if fields[0].isdigit():
        word = fields[1].lower()  # !! lc here
        translation = word
        if word in lexicon:
            translation = lexicon[word]
        elif not word in en_words:
            for src, tgt in rules:
                word = re.sub(src, tgt, word)
                if word in en_words:
                    #sys.stderr.write(word + '\n')
                    translation = word
                    break
        fields[1] = translation
        print(*fields, sep='\t')
    else:
        print(line)

