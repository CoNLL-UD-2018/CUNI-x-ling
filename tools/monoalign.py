#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
import sys
from collections import defaultdict, Counter
from pyjarowinkler import distance
from unidecode import unidecode
import re
from functools import lru_cache
import math

# usage: ./monoalign.py src_sentences tgt_sentences lextable,txt > # alignment.align

# add this to counts
# SMOOTH = 0.1

# importance of length match
# LENIMP = 0.2

# max number of translation options for a word
ALIGNED_WORDS = 1

DEBUG = 1

ALIGN_OUTPUT = 2

vowels = r"[aeiouy]"

counts_src = Counter()
counts_tgt = Counter()
cooccurences = Counter()

def init(srcfile, tgtfile):
    global cooccurences, counts_src, counts_tgt
    with open(srcfile, "r") as srcfile_f, open(tgtfile, "r") as tgtfile_f:
        for srcsent, tgtsent in zip(srcfile_f, tgtfile_f):
            srctokens = srcsent.split()
            tgttokens = tgtsent.split()
            for src_word in srctokens:
                counts_src[src_word] += 1
                for tgt_word in tgttokens:
                    cooccurences[(src_word, tgt_word)] += 1
            for tgt_word in tgttokens:
                counts_tgt[tgt_word] += 1
                        
@lru_cache(maxsize=1024)
def isvow(char):
    return re.search(vowels, unidecode(char))

@lru_cache(maxsize=65536)
def deacc_dewov(word):
    deacc = unidecode(word)
    devow = ""
    for char in word:
        if not isvow(char):
            devow += char
    dd = re.sub(vowels, "", deacc)
    return (deacc, devow, dd, dd[:2], len(dd))

# Jaro Winkler that can take emtpy words
SMOOTH=0.01
@lru_cache(maxsize=65536)
def jw_safe(srcword, tgtword):
    if srcword == '' or tgtword == '':
        # 1 if both empty
        # 0.5 if one is length 1
        # 0.33 if one is length 2
        # ...
        return 1/(len(srcword)+len(tgtword)+1)
    elif srcword == tgtword:
        return 1
    else:
        dist = distance.get_jaro_distance(srcword, tgtword)
        if dist > 0:
            return dist
        else:
            return SMOOTH

@lru_cache(maxsize=1024)
def lensim(srclen, tgtlen):
    # return 1/(1 + LENIMP*abs(srclen-tgtlen))
    return 1/(1 + abs(srclen-tgtlen))

@lru_cache(maxsize=1024)
def relposition(position, length):
    if length == 1:
        return 0.5
    else:
        return position/(length-1)

def diagsim(srclen, tgtlen, srcword_index, tgtword_index):
    return 1-abs(relposition(srcword_index, srclen)
            - relposition(tgtword_index, tgtlen))


def dicesim(srcword, tgtword):
    return 2*cooccurences[(srcword,tgtword)] / (
            counts_src[srcword] + counts_tgt[tgtword])

# @lru_cache(maxsize=1024)
def simscore(srctokens, tgttokens, srcword_index, tgtword_index):
    srcword = srctokens[srcword_index]
    tgtword = tgttokens[tgtword_index]
    src_dd = deacc_dewov(srcword)
    tgt_dd = deacc_dewov(tgtword)
    if DEBUG >= 2:
        print("WORDS: " + srcword + " " + tgtword, file=sys.stderr)
        print("deacc: " + src_dd[0] + " " + tgt_dd[0], file=sys.stderr)
        print("devow: " + src_dd[1] + " " + tgt_dd[1], file=sys.stderr)
        print("deacc devow: " + src_dd[2] + " " + tgt_dd[2], file=sys.stderr)

    sim = 1

    diag_sim = diagsim(len(srctokens), len(tgttokens), srcword_index, tgtword_index)
    if DEBUG >= 2:
        print("diagsim  : " + str(diag_sim), file=sys.stderr)
    sim *= diag_sim

    len_sim = lensim(len(srcword), len(tgtword))
    if DEBUG >= 2:
        print("lensim  : " + str(len_sim), file=sys.stderr)
    sim *= len_sim
    
    dvlen_sim = lensim(len(src_dd[1]), len(tgt_dd[1]))
    if DEBUG >= 2:
        print("dvlensim: " + str(dvlen_sim), file=sys.stderr)
    sim *= dvlen_sim

    dice_sim = dicesim(srcword, tgtword)
    if DEBUG >= 2:
        print("dicesim  : " + str(dice_sim), file=sys.stderr)
    sim *= dice_sim

    # TODO have to keep separate counts for that
    # dice_sim_deacc_devow = dicesim(src_dd[2], tgt_dd[2])
    # sim *= dice_sim_deacc_devow

    jw_sim = jw_safe(srcword, tgtword)
    if DEBUG >= 2:
        print("jwsim  : " + str(jw_sim), file=sys.stderr)
    sim *= jw_sim
    
    jw_sim_deacc = jw_safe(src_dd[0], tgt_dd[0])
    if DEBUG >= 2:
        print("jwsimda: " + str(jw_sim_deacc), file=sys.stderr)
    sim *= jw_sim_deacc
    
    jw_sim_devow = jw_safe(src_dd[1], tgt_dd[1])
    if DEBUG >= 2:
        print("jwsimdv: " + str(jw_sim_devow), file=sys.stderr)
    sim *= jw_sim_devow
    
    jw_sim_deacc_devow = jw_safe(src_dd[2], tgt_dd[2])
    if DEBUG >= 2:
        print("jwsimdd: " + str(jw_sim_deacc_devow), file=sys.stderr)
    sim *= jw_sim_deacc_devow
    
    if DEBUG >= 2:
        print("sim    : " + str(sim), file=sys.stderr)
    return sim


alignment_word = defaultdict(Counter)

def align(srctokens, tgttokens):
    global alignment_word

    # compute alignment scores
    matrix = dict()
    for srcword_index in range(len(srctokens)):
        for tgtword_index in range(len(tgttokens)):
            matrix[(srcword_index, tgtword_index)] = simscore(
                    srctokens, tgttokens, srcword_index, tgtword_index)

    # find alignment
    alignment = [ [(-1,0) for x in range(len(srctokens))],
                  [(-1,0) for x in range(len(tgttokens))] ]
    for (srcword_index, tgtword_index) in sorted(matrix, key=matrix.get, reverse=True):
        if (alignment[0][srcword_index] == (-1,0)
                and alignment[1][tgtword_index] == (-1,0)):
            score = matrix[(srcword_index,tgtword_index)]
            alignment[0][srcword_index] = (tgtword_index,score)
            alignment[1][tgtword_index] = (srcword_index,score)
            alignment_word[srctokens[srcword_index]][tgttokens[tgtword_index]] += 1

    return alignment

def print_alignment(sent_index, srctokens, tgttokens, alignment):
    if ALIGN_OUTPUT == 1:
        print(sent_index)
        print(str(len(srctokens)) + " "
                + " ".join(srctokens) + "  # "
                + " ".join([str(x+1) for (x,_) in alignment[0]]) + "  # "
                + " ".join([str(x)   for (_,x) in alignment[0]]))
        print(str(len(tgttokens)) + " "
                + " ".join(tgttokens) + "  # "
                + " ".join([str(x+1) for (x,_) in alignment[1]]) + "  # "
                + " ".join([str(x)   for (_,x) in alignment[1]]))
    elif ALIGN_OUTPUT == 2:
        print(" ".join([str(s)+"-"+str(t)
            for s,(t,_) in enumerate(alignment[0])
            if t != -1]))


def align_files(srcfile, tgtfile):
    sent_index = 0
    with open(srcfile, "r") as srcfile_f, open(tgtfile, "r") as tgtfile_f:
        for srcsent, tgtsent in zip(srcfile_f, tgtfile_f):
            srctokens = srcsent.split()
            tgttokens = tgtsent.split()
            alignment = align(srctokens, tgttokens)
            print_alignment(sent_index, srctokens, tgttokens, alignment)
            if DEBUG >= 1:
                print("aligned sent " + str(sent_index), file=sys.stderr)
            sent_index += 1

# Produces Moses lex format
# Moses phrase table format:
# Ach ||| pravdepodobne ||| 0.000245278 0.0002059 0.000262536 0.0001978 ||| 0-0 ||| 4077 3809 1 ||| |||
# Moses lex table format:
# šľachetného šlechetného 0.4285714
def save_trtable(trtable_file):
    with open(trtable_file, "w") as trtable:
        for srcword in alignment_word:
            total = sum(alignment_word[srcword].values())
            for (tgtword,count) in alignment_word[srcword].most_common(ALIGNED_WORDS):
                print(" ".join([srcword, tgtword, str(count/total)]), file=trtable)

if __name__ == "__main__":
    if DEBUG >= 1:
        print("INITING...", file=sys.stderr)
    init(sys.argv[1], sys.argv[2])
    
    if DEBUG >= 1:
        print("ALIGNING...", file=sys.stderr)
    align_files(sys.argv[1], sys.argv[2])

    if len(sys.argv) > 3:
        if DEBUG >= 1:
            print("SAVING...", file=sys.stderr)
        save_trtable(sys.argv[3])

