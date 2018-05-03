#!/usr/bin/env python3
#coding: utf-8

import sys
import monotranslate

monotranslate.init(sys.argv[1], sys.argv[2])
monotranslate.DEBUG=2
monotranslate.translate(sys.argv[3])

