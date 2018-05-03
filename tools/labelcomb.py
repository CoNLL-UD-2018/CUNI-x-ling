#!/usr/bin/env python3

import sys
from collections import Counter

# inputs
arg_groups = 2 if sys.argv[0].endswith('weighted.py') else 1
label_field = int(sys.argv[1])-1 # 1-based, 4=pos, 8=deprel
# TODO optionally only combine if head matches... which would need adding the
# output (parsed) file as another parameter
N = (len(sys.argv)-2)/arg_groups
assert int(N) == N
N = int(N)
inputs = list()
for f in sys.argv[2:N+2]:
    inputs.append(open(f))
if arg_groups == 1:
    weights = [1] * N
else:
    weights = [float(w) for w in sys.argv[N+2:2*N+2]]

# iterate in reverse order so that "fields" get remembered from the first input
inputs.reverse()
weights.reverse()

end_of_file = 0
while not end_of_file:
    # read in the next line from each file
    # special lines set special flags,
    # standard lines fill "labels" and "fields"
    end_of_sentence = 0
    comment = 0
    labels = Counter()
    for fh, weight in zip(inputs, weights):
        line = fh.readline()
        if not line:
            # end of file
            end_of_file += 1
        elif line == '\n':
            # end of sentence
            end_of_sentence += 1
        elif line.startswith('#'):
            # comment
            comment += 1
        else:
            fields = line.strip().split('\t')
            label = fields[label_field]
            labels[label] += weight
    # process fields and labels, unless in a special state
    if end_of_file:
        assert end_of_file == N, 'files must have same length'
    elif end_of_sentence:
        assert end_of_sentence == N, 'sentences must have same length in all files'
        print()
    elif comment:
        # TODO this is stupid
        assert comment == N, 'identical positioning of comments expected'
    else:
        assert fields
        assert labels
        label = labels.most_common(1)[0][0]
        fields[label_field] = label
        print(*fields, sep='\t')

for fh in inputs:
    fh.close()
