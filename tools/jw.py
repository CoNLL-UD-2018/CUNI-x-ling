#!/usr/bin/env python3

import sys
from pyjarowinkler import distance

print(sys.argv[1])
print(sys.argv[2])
print(distance.get_jaro_distance(sys.argv[1], sys.argv[2]))

