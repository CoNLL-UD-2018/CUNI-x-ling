#!/usr/bin/env python3
#coding: utf-8

import sys
# from collections import defaultdict

# parameters: languages_list ranking iso

# read in language families
with open(sys.argv[1]) as languages_file:
    families = dict()
    for line in languages_file:
        iso, genus, family = line.strip().split(',')
        families[iso] = (family, genus)

target = sys.argv[3]

if not target in families:
    sys.exit()

# eval the ranking
# format: 1 iso per line
total = 0
bad = 0
with open(sys.argv[2]) as ranking_file:
    (target_family, target_genus) = families[target]
    print(target, target_family, target_genus)
    prev_genus_match = True
    prev_family_match = True
    for line in ranking_file:
        total += 1
        iso = line.strip()
        if iso in families:
            (family, genus) = families[iso]
            print(iso, family, genus)
            if genus == target_genus:
                if not prev_genus_match:
                    bad += 1
                prev_genus_match = True
                prev_family_match = True
            elif family == target_family:
                if not prev_family_match:
                    bad += 1
                prev_genus_match = False
                prev_family_match = True
            else:
                prev_genus_match = False
                prev_family_match = False

acc = (total-bad)/total
print('Total:', total, 'Bad:', bad, 'Accuracy:', acc)

