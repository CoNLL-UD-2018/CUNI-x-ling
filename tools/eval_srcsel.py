#!/usr/bin/env python3
#coding: utf-8

# usage: script.py oracle_LAS.tsv predicted_sim.tsv

import sys
import scipy.stats
import argparse
parser = argparse.ArgumentParser(
        description="compute source selection accuracy; data format: TSV files, first column is language code, second column is a float similarity"
        )
parser.add_argument("oraclefile", help="delex las scores (oracle similarity)")
parser.add_argument("predictedfile", help="predicted similarities")
parser.add_argument("-N", type=int,
    help="look at the N most similar langs (default=1)", default=1)
parser.add_argument("-u", "--unweighted",
    help="do not weight the N langs by their similarity scores",
    action="store_true")
parser.add_argument("-c", "--correlation",
    help="compute Pearsons r on the oracle las vs predicted sim",
    action="store_true")
parser.add_argument("--wo",
    help="weight the oracle by relative las",
    action="store_true")
parser.add_argument("-s", "--simple",
    help="second param is just 1 lang code",
    action="store_true")
args = parser.parse_args()

lang2las = dict()
best_las = 0
with open(args.oraclefile) as oraclefh:
    for line in oraclefh:
        lang, las = line.split()
        las = float(las)
        if las > best_las:
            best_las = las
        lang2las[lang] = las

weighted_oracle_las = best_las
if args.wo:
    with open(args.oraclefile) as oraclefh:
        nominator = 0
        denominator = 0
        for i in range(args.N):
            line = oraclefh.readline()
            lang, las = line.split()
            las = float(las)
            weight = las/best_las
            nominator += weight * las
            denominator += weight
        weighted_oracle_las = nominator/denominator

if args.simple:
    lang = args.predictedfile
    result = lang2las[lang]/weighted_oracle_las
    print(result)
    sys.exit()

with open(args.predictedfile) as predictedfh:
    if args.correlation:
        predicted_list = list()
        oracle_list = list()
        for i in range(args.N):
            line = predictedfh.readline()
            lang, sim = line.split()
            sim = float(sim)
            predicted_list.append(sim)
            oracle_list.append(lang2las[lang])
        r, p = scipy.stats.pearsonr(oracle_list, predicted_list)
        print(r)
    else:
        nominator = 0
        denominator = 0
        for i in range(args.N):
            line = predictedfh.readline()
            lang, sim = line.split()
            sim = float(sim)
            if args.unweighted:
                sim = 1
            nominator += sim * lang2las[lang]
            denominator += sim
        result = nominator/denominator/weighted_oracle_las
        print(result)

