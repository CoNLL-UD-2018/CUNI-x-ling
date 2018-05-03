#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
import sys
from pyjarowinkler import distance
from unidecode import unidecode
import re
from functools import lru_cache
import math
from monotr_lm import LM

# usage: ./monotranslate.py src.freqlist tgt.freqlist < src_input > tgt_output

# add this to counts
SMOOTH = 0.1

# do not care much for frequency similarity
# once it is above this
FREQSIM_THRESH = 0.5

# importance of length match
LENIMP = 0.2

# no oovs = init with src, oovs = put "__OOV__"
OOV = 0

# try all translation options -- don't use lossy pruning (for small datasets)
TRY_ALL = 0

DEBUG = 1

USE_LM = True

ADD_LM = True

vowels = r"[aeiouy]"

srclist = None
tgtlist = None
lm = LM()

def init(srclistfile, tgtlistfile, lmfile=None):
    global srclist, tgtlist, lm
    with open(srclistfile,"rb") as packed:
        srclist = msgpack.load(packed, encoding="utf-8", use_list=False)
    with open(tgtlistfile,"rb") as packed:
        tgtlist = msgpack.load(packed, encoding="utf-8", use_list=False)
    if lmfile is not None:
        lm.load(lmfile)

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

@lru_cache(maxsize=1024)
def srcwordfreq(word):
    return (wordcount(word, srclist) + SMOOTH) / srclist[None][None]

@lru_cache(maxsize=65536)
def tgtwordfreq(word):
    return (wordcount(word, tgtlist) + SMOOTH) / tgtlist[None][None]

def wordcount(word, wordlist):
    (_, _, _, prefix, length) = deacc_dewov(word)
    key = (prefix, length)
    if key in wordlist and word in wordlist[key]:
        return wordlist[key][word]
    else:
        return 0

@lru_cache(maxsize=65536)
def sortedtgtdict(prefix, tgt_length):
    d = tgtlist[(prefix,tgt_length)]
    return sorted(d, key=d.get, reverse=True)

@lru_cache(maxsize=65536)
def translate(srcword, prevs):
    if OOV:
        tgt_best = "__OOV__"
        tgt_best_score = 0
    else:
        # init with keeping the original word
        tgt_best = srcword
        tgt_best_score = simscore(srcword, srcword, prevs)
    if DEBUG >= 1:
        print("SRC: " + srcword + " TGT: " + tgt_best + " "
                + str(tgt_best_score), file=sys.stderr)
    if TRY_ALL:
        for key in tgtlist:
            if key != None:
                (tgt_best, tgt_best_score) = translate_internal(
                        srcword, prevs, key[0], key[1], tgt_best, tgt_best_score)
    else:
        (_, _, _, prefix, src_length) = deacc_dewov(srcword)
        for tgt_length in [src_length, src_length-1, src_length+1]:
            if (prefix,tgt_length) not in tgtlist:
                continue
            (tgt_best, tgt_best_score) = translate_internal(
                    srcword, prevs, prefix, tgt_length, tgt_best, tgt_best_score)
        if (lm.valid and ADD_LM):
            if DEBUG >= 1:
                print("add lm cands", file=sys.stderr)
            for tgtword in lm.generate(prevs):
                if DEBUG >= 2:
                    print("lm cand: " + tgtword, file=sys.stderr)
                (tgt_best, tgt_best_score) = translate_try(
                        srcword, tgtword, prevs, tgt_best, tgt_best_score)
    return (tgt_best, tgt_best_score)

def translate_internal(srcword, prevs, prefix, tgt_length, tgt_best, tgt_best_score):
    # traverse from more frequent to less frequent with early stopping
    for tgtword in sortedtgtdict(prefix, tgt_length):
        if DEBUG >= 2:
            print("TGT: " + tgtword + " count: "
                    + str(wordcount(tgtword, tgtlist)), file=sys.stderr)
        if freqsim(srcword, tgtword) < tgt_best_score:
            # no need to go on, cannot be better than current best
            if tgtwordfreq(tgtword) < srcwordfreq(srcword):
                # too infrequent, stop processing this list
                break
            else:
                # too frequent, move on in the list
                continue
        # "else" -- passed frequency check
        (tgt_best, tgt_best_score) = translate_try(
                srcword, tgtword, prevs, tgt_best, tgt_best_score)
    return (tgt_best, tgt_best_score)

def translate_try(srcword, tgtword, prevs, tgt_best, tgt_best_score):
    score = simscore(srcword, tgtword, prevs, tgt_best_score)
    if score > tgt_best_score:
        tgt_best = tgtword
        tgt_best_score = score
        if DEBUG >= 1:
            print("SRC: " + srcword + " TGT: " + tgt_best + " "
                    + str(tgt_best_score), file=sys.stderr)
    return (tgt_best, tgt_best_score)

# Jaro Winkler that can take emtpy words
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
        return distance.get_jaro_distance(srcword, tgtword)

@lru_cache(maxsize=16)
def freqsim(srcword, tgtword):
    src_freq = srcwordfreq(srcword)
    tgt_freq = tgtwordfreq(tgtword)
    freq_sim = 1/(1+abs(math.log(src_freq)-math.log(tgt_freq)))
    if DEBUG >= 2:
        print("SRC: " + srcword, file=sys.stderr)
        print("TGT: " + tgtword, file=sys.stderr)
        print("count: " + str(wordcount(srcword, srclist)) + " freq: "
                + str(src_freq), file=sys.stderr)
        print("count: " + str(wordcount(tgtword, tgtlist)) + " freq: "
                + str(tgt_freq), file=sys.stderr)
        print("freqsim: " + str(freq_sim), file=sys.stderr)
    if freq_sim > FREQSIM_THRESH:
        freq_sim = FREQSIM_THRESH + 0.1*(freq_sim-FREQSIM_THRESH)
    return freq_sim

@lru_cache(maxsize=1024)
def lensim(srclen, tgtlen):
    return 1/(1 + LENIMP*abs(srclen-tgtlen))

# early stopping once similarity falls bellow current best
# (jw is costly)
@lru_cache(maxsize=1024)
def simscore(srcword, tgtword, prevs, current_best_score=0):
    freq_sim = freqsim(srcword, tgtword)
    src_dd = deacc_dewov(srcword)
    tgt_dd = deacc_dewov(tgtword)
    if DEBUG >= 2:
        print("deacc: " + src_dd[0] + " " + tgt_dd[0], file=sys.stderr)
        print("devow: " + src_dd[1] + " " + tgt_dd[1], file=sys.stderr)
        print("deacc devow: " + src_dd[2] + " " + tgt_dd[2], file=sys.stderr)
    sim = freq_sim

    len_sim = lensim(len(srcword), len(tgtword))
    if DEBUG >= 2:
        print("lensim  : " + str(len_sim), file=sys.stderr)
    sim *= len_sim
    if sim < current_best_score:
        return sim
    
    dvlen_sim = lensim(len(src_dd[1]), len(tgt_dd[1]))
    if DEBUG >= 2:
        print("dvlensim: " + str(dvlen_sim), file=sys.stderr)
    sim *= dvlen_sim
    if sim < current_best_score:
        return sim
    
    jw_sim = jw_safe(srcword, tgtword)
    if DEBUG >= 2:
        print("jwsim  : " + str(jw_sim), file=sys.stderr)
    sim *= jw_sim
    if sim < current_best_score:
        return sim
    
    jw_sim_deacc = jw_safe(src_dd[0], tgt_dd[0])
    if DEBUG >= 2:
        print("jwsimda: " + str(jw_sim_deacc), file=sys.stderr)
    sim *= jw_sim_deacc
    if sim < current_best_score:
        return sim
    
    jw_sim_devow = jw_safe(src_dd[1], tgt_dd[1])
    if DEBUG >= 2:
        print("jwsimdv: " + str(jw_sim_devow), file=sys.stderr)
    sim *= jw_sim_devow
    if sim < current_best_score:
        return sim
    
    jw_sim_deacc_devow = jw_safe(src_dd[2], tgt_dd[2])
    if DEBUG >= 2:
        print("jwsimdd: " + str(jw_sim_deacc_devow), file=sys.stderr)
    sim *= jw_sim_deacc_devow
    if sim < current_best_score:
        return sim
   
    # TODO maybe move up?
    # TODO not sure about early stopping now
    lm_score = 1
    if lm.valid and USE_LM:
        lm_score = lm.score(prevs, tgtword)**0.25  # 4th root
        if DEBUG >= 2:
            print("lmscore: " + str(lm_score), file=sys.stderr)
    sim *= lm_score
    if sim < current_best_score:
        return sim
    
    if DEBUG >= 2:
        print("sim    : " + str(sim), file=sys.stderr)
    return sim

# prevs must already be lc'd
def translatecased(word, prevs):
    (translation, score) = translate(word.lower(), prevs)
    # if prevs not lc'd:  tuple(p.lower() for p in prevs)
    if(word.istitle()):
        translation = translation.title()
    if(word.isupper()):
        translation = translation.upper()
    return (translation, score)

def translateline(line):
    prevs = lm.prevdeque()
    translation = []
    for word in line.split():
        word_translation = translatecased(word, tuple(prevs))[0]
        translation.append(word_translation)
        prevs.append(word_translation.lower())
    return " ".join(translation)

def processtbline(line):
    assert False
    line = line.rstrip('\n')
    if line != '' and not line.startswith('#'):
        fields = line.split('\t')
        return fields
    else:
        return None

# TODO keep previous translations in prevs (just the words, lc'd)
def translatetbline(line, prevs):
    assert False
    # TODO implement
    #fields = processtbline(line)
    #prevtgtfields = processtbline(prevtgtline)
    #if fields is not None:
    #    if prevtgtfields is not None:
    #        (fields[1], score) = translatecased(fields[1], prevtgtfields[1])
    #    else:
    #        (fields[1], score) = translatecased(fields[1], START)
    #    return('\t'.join(fields), score, 1)
    #else:
    #    return(line, 0, 0)

if __name__ == "__main__":
    if (len(sys.argv)) >= 4:
        init(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        init(sys.argv[1], sys.argv[2])
    for line in sys.stdin:
        print(translateline(line))

