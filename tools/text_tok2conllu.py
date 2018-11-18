#!/usr/bin/env python3
#coding: utf-8

import sys

textfile, tokfile = sys.argv[1:3]

fill = '\t'.join(7 * ['_'])

with open(textfile) as text, open(tokfile) as tok:
    for line_text, line_tok in zip(text, tok):
        # - assume that line_text and line_tok differ only in whitespace
        # - assume no token in line_tok contains spaces,
        # i.e. all spaces from line_text are preserved
        # - assume all comments in CoNLLU files are voluntary
        position = 0  # in line_text
        token_id = 0
        for token in line_tok.strip('\n').split(' '):
            if token == '':
                continue

            token_id += 1

            new_position = position + len(token)
            assert line_text[position:new_position] == token, "!!=!!".join((
                line_text, line_tok, line_text[position:new_position], token))
            position = new_position

            misc = 'SpaceAfter=No'
            if line_text[position] == ' ':
                misc = '_'
                position += 1
            elif line_text[position] == '\n':
                misc = '_'
                # TODO should check that at end of line_tok

            print(token_id, token, fill, misc, sep='\t')
        print()

