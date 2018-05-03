#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate

monotranslate.init(sys.argv[1], sys.argv[2])
monotranslate.DEBUG = 0

sumscore = 0
countlines = 0
for line in sys.stdin:
    (translation, score, count) = monotranslate.translatetbline(line)
    sumscore += score
    countlines += count
    print(translation)
print("avgscore: " + str(sumscore/countlines), file=sys.stderr)

