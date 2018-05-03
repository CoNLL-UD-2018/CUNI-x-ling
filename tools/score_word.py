#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate

monotranslate.init(sys.argv[1], sys.argv[2])
monotranslate.DEBUG=2
monotranslate.simscore(sys.argv[3], sys.argv[4])
monotranslate.simscore(sys.argv[3], sys.argv[5])

