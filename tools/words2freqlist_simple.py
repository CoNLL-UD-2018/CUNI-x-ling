#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
from collections import defaultdict, Counter
import sys

class Freqlist:

    def __init__(self):
        self.freqlist = Counter()
    
    def add(self, word):
        word = word.lower()
        self.freqlist[word] += 1
        self.freqlist[None] += 1
    
    def addtbline(self, line):
        line = line.rstrip('\n')
        if line != '' and not line.startswith('#'):
            fields = line.split('\t')
            self.add(fields[1])
    
    def addline(self, line):
        line = line.rstrip('\n')
        words = line.split(' ')
        for word in words:
            self.add(word)
    
    def readin(self, filename):
        with open(filename, "r") as infile:
            for line in infile:
                self.add(line.rstrip())
    
    def writeout(self, filename):
        with open(filename, "wb") as outfile:
            msgpack.dump(self.freqlist, outfile)

if __name__ == "__main__":
    f = Freqlist()
    f.readin(sys.argv[1])
    f.writeout(sys.argv[2])
