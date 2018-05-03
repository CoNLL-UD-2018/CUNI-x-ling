#!/usr/bin/env python3
#coding: utf-8

import sys
from collections import defaultdict
import warnings

# TODO: now unweighted, implement weighted

# TODO: now unlabelled, implement labelled

# inputs
inputs = list()
for f in sys.argv[1:]:
    inputs.append(open(f))

def get_sentence(i):
    sentence = list()
    full_sentence = list()
    for line in i:
        line = line.strip()
        if line.startswith('#'):
            # comment
            pass
        elif not line:
            # end of sentence
            break
        else:
            fields = line.split('\t')
            # parent, child
            sentence.append((int(fields[6]), int(fields[0])))
            full_sentence.append(fields)
    return (sentence, full_sentence)

# Adapted from https://github.com/mlbright/edmonds.git
# --------------------------------------------------------------------------------- #

def _reverse(graph):
    r = {}
    for src in graph:
        for (dst,c) in list(graph[src].items()):
            if dst in r:
                r[dst][src] = c
            else:
                r[dst] = { src : c }
    return r

def _getCycle(n, g, visited=None, cycle=None):
    if visited is None:
        visited = set()
    if cycle is None:
        cycle = []
    visited.add(n)
    cycle += [n]
    if n not in g:
        return cycle
    for e in g[n]:
        if e not in visited:
            cycle = _getCycle(e,g,visited,cycle)
    return cycle

def _mergeCycles(cycle,G,RG,g,rg):
    allInEdges = []
    minInternal = None
    minInternalWeight = sys.maxsize

    # find minimal internal edge weight
    for n in cycle:
        for e in RG[n]:
            if e in cycle:
                if minInternal is None or RG[n][e] < minInternalWeight:
                    minInternal = (n,e)
                    minInternalWeight = RG[n][e]
                    continue
            else:
                allInEdges.append((n,e))        

    # find the incoming edge with minimum modified cost
    minExternal = None
    minModifiedWeight = 0
    for s,t in allInEdges:
        u,v = rg[s].popitem()
        rg[s][u] = v
        w = RG[s][t] - (v - minInternalWeight)
        if minExternal is None or minModifiedWeight > w:
            minExternal = (s,t)
            minModifiedWeight = w

    u,w = rg[minExternal[0]].popitem()
    rem = (minExternal[0],u)
    rg[minExternal[0]].clear()
    if minExternal[1] in rg:
        rg[minExternal[1]][minExternal[0]] = w
    else:
        rg[minExternal[1]] = { minExternal[0] : w }
    if rem[1] in g:
        if rem[0] in g[rem[1]]:
            del g[rem[1]][rem[0]]
    if minExternal[1] in g:
        g[minExternal[1]][minExternal[0]] = w
    else:
        g[minExternal[1]] = { minExternal[0] : w }

# --------------------------------------------------------------------------------- #

def mst(root,G):
    """ The Chu-Lui/Edmond's algorithm

    arguments:

    root - the root of the MST
    G - the graph in which the MST lies

    returns: a graph representation of the MST

    Graph representation is the same as the one found at:
    http://code.activestate.com/recipes/119466/

    Explanation is copied verbatim here:

    The input graph G is assumed to have the following
    representation: A vertex can be any object that can
    be used as an index into a dictionary.  G is a
    dictionary, indexed by vertices.  For any vertex v,
    G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of
    the edge.  This is related to the representation in
    <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs
    as dictionaries mapping vertices to lists of neighbors,
    however dictionaries of edges have many advantages
    over lists: they can store extra information (here,
    the lengths), they support fast existence tests,
    and they allow easy modification of the graph by edge
    insertion and removal.  Such modifications are not
    needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph
    represented as described here could be handed without
    modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects;
    they can be any other object that obeys dict protocol,
    for instance a wrapper in which vertices are URLs
    and a call to G[v] loads the web page and finds its links.
    """

    RG = _reverse(G)
    if root in RG:
        RG[root] = {}
    g = {}
    for n in RG:
        if len(RG[n]) == 0:
            continue
        minimum = sys.maxsize
        s,d = None,None
        for e in RG[n]:
            if RG[n][e] < minimum:
                minimum = RG[n][e]
                s,d = n,e
        if d in g:
            g[d][s] = RG[s][d]
        else:
            g[d] = { s : RG[s][d] }
            
    cycles = []
    visited = set()
    for n in g:
        if n not in visited:
            cycle = _getCycle(n,g,visited)
            cycles.append(cycle)

    rg = _reverse(g)
    for cycle in cycles:
        if root in cycle:
            continue
        _mergeCycles(cycle, G, RG, g, rg)

    return g

# --------------------------------------------------------------------------------- #

while True:
    # input_graph[parent][child] = weight
    input_graph = defaultdict(lambda : defaultdict(int))
    for i in inputs:
        (sentence, full_sentence) = get_sentence(i)
        for (parent, child) in sentence:
            input_graph[parent][child] += 1
    if not input_graph:
        # no more input
        break
    else:
        mst_graph = _reverse(mst(0, input_graph))
        for line in full_sentence:
            child = int(line[0])
            parent = list(mst_graph[child].keys())[0]
            line[6] = str(parent)
            print(*line, sep='\t')
            if len(mst_graph[child].keys()) != 1:
                warnings.warn("weird number of parents: " + str(len(mst_graph[child].keys())))
        print()

# wrap up
for i in inputs:
    i.close()


