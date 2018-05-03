#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use autodie;

use Graph;
use Graph::Directed;
use Graph::ChuLiuEdmonds;

if ( @ARGV != 0 ) {
    die("Usage: $0 < graphs > MSTs \n");
}

while (<>) {
    chomp;
    my @input = split;
    if (@input) {
        my $N = shift @input;
        # parent child weight parent child weight ...
        my @edges = @input;
        my $graph = Graph::Directed->new(vertices=>[(1 .. $N)]);
        $graph->add_weighted_edges(@edges);
    
        my $msts = $graph->MST_ChuLiuEdmonds($graph);

        my @parents = (0) x ($N+1);
        foreach my $edge ($msts->edges) {
            $parents[$edge->[1]] = $edge->[0];
        }
        # array 0-based but children 1-based
        shift @parents;
        print join ' ', @parents;
    }
    print "\n";
}

