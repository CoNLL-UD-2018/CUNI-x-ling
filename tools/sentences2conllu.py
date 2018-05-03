#!/usr/bin/env python3
#coding: utf-8

import sys

EMPTY = '_'

inputs = [open(filename) if filename != '_' else None for filename in sys.argv[1:]]

def get_lines(inputs):
    # read in from files
    missing_input = True
    while missing_input:
        missing_input = False
        lines = list()
        length = -1
        for i in inputs:
            if i == None:
                lines.append(None)
            else:
                line = i.readline()
                if line == '':
                    # end
                    return (None, None)
                elif line == '\n':
                    # missing input
                    # but need to finish the cycle to keep lines in sync
                    missing_input = True
                else:
                    lines.append(line.split())
                    length = len(lines[-1])
    # add underscores
    result = list()
    for l in lines:
        if l == None:
            result.append([EMPTY] * length)
        else:
            assert len(l) == length, "line must have same length in all inputs"
            result.append(l)
    return (result, length)

while True:    
    (lines, length) = get_lines(inputs)
    if lines:
        for index in range(length):
            output = list()
            output.append(index+1) # 1-based ord
            for l in lines:
                output.append(l[index])
            print(*output, sep='\t')
        print()
    else:
        # end
        for i in [i for i in inputs if i]:
            assert i.readline() == '', "inputs must have the same length"
        break

for i in inputs:
    if i != None:
        i.close()

