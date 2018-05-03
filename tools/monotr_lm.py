#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
from collections import defaultdict, Counter, deque
import sys
import itertools
from heapq import nlargest

class LM:

    valid = False

    # start of sentence symbol
    START = "[START]"

    # ngram size
    N = 3

    # minimum count of ngram to remember it
    MINCOUNT = 2

    # suggest this many translaton candidates by the LM
    GENERATE_N = 20

    # probability of unseen ngrams
    SMOOTH = 0.001

    def __init__(self):
        self.ngrams = defaultdict(lambda : Counter())
    
    def lastntuple(self, deq, n):
        return tuple(itertools.islice(deq, len(deq)-n))

    def add(self, word, prevs):
        for n in range(1, LM.N):
            index = prevs[-n:]
            self.ngrams[index][word] += 1

    def prevdeque(self):
        """Generate a deque of N-1 START symbols."""
        return deque([LM.START] * (LM.N-1), maxlen=LM.N-1)
    
    def readin_words(self, filename):
        with open(filename, "r") as infile:
            # maxlen: autodiscard surplus items
            prevs = self.prevdeque()
            for line in infile:
                word = line.rstrip().lower()
                self.add(word, tuple(prevs))
                prevs.append(word)
        self.valid = True

    def readin_sentences(self, filename):
        with open(filename, "r") as infile:
            for line in infile:
                prevs = self.prevdeque()
                for word in line.rstrip().lower().split():
                    self.add(word, tuple(prevs))
                    prevs.append(word)
        self.valid = True

    def filter(self):
        for prevs in self.ngrams:
            for word in list(self.ngrams[prevs].keys()):
                if self.ngrams[prevs][word] < LM.MINCOUNT:
                    del self.ngrams[prevs][word]
    
    def writeout(self, filename):
        with open(filename, "wb") as outfile:
            msgpack.dump(self.ngrams, outfile)

    def load(self, filename):
        with open(filename,"rb") as packed:
            self.ngrams = msgpack.load(packed, encoding="utf-8", use_list=False)
        self.valid = True

    def generate(self, prevs):
        for n in range(LM.N-1, 0, -1):
            index = prevs[-n:]
            if index in self.ngrams:
                return nlargest(LM.GENERATE_N, self.ngrams[index].keys(),
                        key=self.ngrams[index].get)
        # big else
        return []

    def score(self, prevs, word):
        """Likelihood of word following prevs; uniform interpolation."""
        total = LM.SMOOTH
        for n in range(LM.N-1, 0, -1):
            index = prevs[-n:]
            if index in self.ngrams and word in self.ngrams[index]:
                divsor = sum(self.ngrams[index].values())
                total += self.ngrams[index][word] / divsor
        return total / (LM.N-1+LM.SMOOTH)

# default: read in text, 1 word per line
if __name__ == "__main__":
    f = LM()
    f.readin_sentences(sys.argv[1])
    f.filter()
    f.writeout(sys.argv[2])
