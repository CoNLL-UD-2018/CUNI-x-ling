#!/usr/bin/env python3

from collections import defaultdict
from collections import Counter
import sys
import pickle
from pyjarowinkler import distance


src_file, tgt_file, align_file, trtable_file = sys.argv[1:5]
#src_file, tgt_file, align_file, trtable_file = [
#        'para/OpenSubtitles2018.fr-br.fr.tokenized',
#        'para/OpenSubtitles2018.fr-br.br.tokenized',
#        'fastwork/fr-br.intersect',
#        'fastwork/fr-br.trtable']

# Get raw ttable
raw_translation_table = defaultdict(Counter)

with open(src_file) as src, open(tgt_file) as tgt, open(align_file) as align:
    for line_src, line_tgt, line_align in zip(src, tgt, align):
        tokens_src = line_src.rstrip().split(' ')
        tokens_tgt = line_tgt.rstrip().split(' ')
        links = line_align.split()
        for link in links:
            id_src, id_tgt = link.split('-')
            token_src = tokens_src[int(id_src)].replace('_', ' ')
            token_tgt = tokens_tgt[int(id_tgt)].replace('_', ' ')
            raw_translation_table[token_src][token_tgt] += 1
            raw_translation_table[token_src.lower()][token_tgt.lower()] += 1

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
pickle.dump(translation_table, open( trtable_file, "wb" ) )

