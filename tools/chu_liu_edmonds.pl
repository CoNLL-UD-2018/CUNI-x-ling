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
    my @input = split / /;
    my $N = shift @input;
    # parent child weight parent child weight ...
    my @edges = @input;
    #print "N=";
    #print($N);
    #print "\n";


    my $graph = Graph::Directed->new(vertices=>[(1 .. $N)]);
    $graph->add_weighted_edges(@edges);
    foreach my $edge ($graph->edges) {
        #print $edge->[0];
        #print " ";
        #print $edge->[1];
        #print "\n";
    }
    my $msts = $graph->MST_ChuLiuEdmonds($graph);
    #print "MST: \n";
    foreach my $edge ($msts->edges) {
        print $edge->[0];  # parent
        print "-";
        print $edge->[1];  # child
        print " ";
    }
    print "\n";
}

