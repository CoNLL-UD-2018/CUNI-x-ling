#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
from collections import defaultdict, Counter
import sys

START = "[START]"

MINCOUNT = 2

class Bigrams:

    def __init__(self):
        self.bigrams = defaultdict(lambda : Counter())
    
    def add(self, word, prev):
        self.bigrams[prev][word] += 1
        self.bigrams[None][None] += 1
    
    def readin(self, filename):
        with open(filename, "r") as infile:
            prev = START
            for line in infile:
                word = line.rstrip().lower()
                self.add(word, prev)
                prev = word

    def filter(self):
        for prev in self.bigrams:
            for word in list(self.bigrams[prev].keys()):
                if self.bigrams[prev][word] < MINCOUNT:
                    del self.bigrams[prev][word]
    
    def writeout(self, filename):
        with open(filename, "wb") as outfile:
            msgpack.dump(self.bigrams, outfile)

# default: read in text, 1 word per line
if __name__ == "__main__":
    f = Bigrams()
    f.readin(sys.argv[1])
    f.filter()
    f.writeout(sys.argv[2])
