#!/usr/bin/env python3
#coding: utf-8

import sys

def shift_i2o(i2o, index):
    index = int(index)
    if index == 0:
        return 0
    else:
        # alignment 0-based, ord 1-based
        return i2o[index-1]+1

(fcol1, fcol2, fcol3, freorder) = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) 
with open(fcol1) as col1, open(fcol2) as col2, open(fcol3) as col3, open(freorder) as reorder:
    for alignment in reorder:
        links = alignment.split();
        #scol1 = list()
        scol2 = list()
        scol3 = list()
        i2o = dict()
        o2i = dict()
        for i in range(len(links)):
            # indices: source-target (I-O)
            (indexI, indexO) = (int(l) for l in links[i].split('-'))
            i2o[indexI] = indexO
            o2i[indexO] = indexI
            #scol1.append(col1.readline().rstrip())
            scol2.append(col2.readline().rstrip())
            scol3.append(col3.readline().rstrip())
        # +1 for empty line -- TODO may be missing at file end!!!
        #scol1.append(col1.readline().rstrip())
        scol2.append(col2.readline().rstrip())
        scol3.append(col3.readline().rstrip())
        for indexO in range(len(scol2)-1):
            # TODO delete multitokens before everything ... not present in EN
            # new ord, 1-based
            indexI = o2i[indexO]
            print(indexO+1, end='\t')
            print(scol2[indexO], end='\t')
            # new parent ord, 1-based
            tcol3 = scol3[indexI].split('\t');
            tcol3[4] = shift_i2o(i2o, tcol3[4])
            print(*tcol3, sep='\t', end='\n')
        print()


