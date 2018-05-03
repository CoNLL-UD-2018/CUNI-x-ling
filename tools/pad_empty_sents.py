#!/usr/bin/env python3
#coding: utf-8

import sys

# this is the dense input to be padded
input_f = sys.argv[1]

# these are the files where empty lines were turned into missing lines in input
control_f = sys.argv[2:]

# open
input_fh = open(input_f)
control_fh = [open(filename) for filename in control_f]

while True:
    control_lines = [fh.readline() for fh in control_fh]
    if control_lines[0] == '':
        # end of control file -> this is the end
        assert input_fh.readline() == '', "input too long"
        for line in control_lines:
            assert line == '', "all controls must have the same length"
        break
    elif [True for line in control_lines if line=='\n']:
        # at least one line is empty -- pad
        print()
    else:
        # no line is empty -- print
        line = input_fh.readline()
        assert line != '', "input too short"
        print(line, end='')

# close
input_fh.close()
for fh in control_fh:
    fh.close()

