#!/usr/bin/env python3
#coding: utf-8

# similarity of src lang to the given tgt lang

# input: wals_file.tsv tgt_lang_wals_code src_lang_wals_code+

# ouput: similarity between 0 and 1 for each src lang

import sys

lang_tgt = sys.argv[2]
langs_src = sys.argv[3:]

# Measure src-tgt similarity
def similarity(fields_src, fields_tgt):
    match = 0
    count = 0
    for (src, tgt) in zip(fields_src, fields_tgt):
        if tgt:
            count += 1
            if tgt == src:
                match += 1
    assert count > 0, "No features defined for source language"
    return match/count

# Find src fields
with open(sys.argv[1]) as wals:
    for line in wals:
        fields = line.rstrip('\n').split('\t')
        if fields[0] == lang_tgt:
            fields_tgt = fields
            break
assert fields_tgt, "Cannot find target language features"

with open(sys.argv[1]) as wals:
    for line in wals:
        fields = line.rstrip('\n').split('\t')
        for lang_src in langs_src:
            if fields[0] == lang_src:
                print(lang_src, similarity(fields, fields_tgt), sep='\t')

