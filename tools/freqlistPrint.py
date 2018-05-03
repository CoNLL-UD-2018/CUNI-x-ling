#!/usr/bin/env python3
#coding: utf-8

import msgpack
import io
from collections import defaultdict
import sys

with open(sys.argv[1],"rb") as packed:
    freqlist=msgpack.load(packed, encoding="utf-8", use_list=False)

print(freqlist)


