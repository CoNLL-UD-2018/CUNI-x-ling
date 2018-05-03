#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle
from pyjarowinkler import distance

raw_translation_table = defaultdict(Counter)

# Get raw ttable

for line in sys.stdin:
    line = line.rstrip('\n')
    if line != '':
        source, target = line.split('\t')
        if (target != ''):
            lsource = source.lower()
            ltarget = target.lower()
            raw_translation_table[source][target] += 1
            raw_translation_table[lsource][ltarget] += 1

# Filter ttable
# Only keep the most frequent entry
# In case of ties, sort by jaro_winkler similarity to source
# In case there are still ties, sort alphabetically
print("Filtering ttable", file=sys.stderr)

def filter_entry(source, raw_table):
    
    # count is the primary criterion
    best_count = 0
    bests = []
    for target in raw_table[source]:
        count = raw_table[source][target]
        if count > best_count:
            best_count = count
            bests = [target]
        elif count == best_count:
            bests.append(target)
    
    # jaro winkler is the secondary criterion
    if len(bests) > 1:
        # alphabetic is the third criterion
        # (this is not meaningful, this is just to be deterministic)
        bests.sort()
        best_jw = -1
        best = None
        source_word = source
        for target in bests:
            jw = distance.get_jaro_distance(source_word, target)
            if jw > best_jw:
                best_jw = jw
                best = target
            # not accounting for ties -- we just take the first one as best
        return best
    else:
        return bests[0]

translation_table = {entry : filter_entry(entry, raw_translation_table)
        for entry in raw_translation_table }

# Save ttable
print("Saving ttable", file=sys.stderr)
pickle.dump(translation_table, open( sys.argv[1], "wb" ) )

