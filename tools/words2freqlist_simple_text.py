#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
from collections import defaultdict, Counter
import sys
from words2freqlist_simple import Freqlist

if __name__ == "__main__":
    f = Freqlist()
    with open(sys.argv[1], "r") as infile:
        for line in infile:
            f.addline(line.rstrip())
    f.writeout(sys.argv[2])
