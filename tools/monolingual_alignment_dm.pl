#!/usr/bin/env perl

use strict;
use warnings;
use Text::JaroWinkler;
use List::Util qw(min max);

binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
binmode STDIN, ":utf8";

my @form;

my $type = 'intersection';

foreach my $f (0, 1) {
    open (TEXT, "<:utf8", $ARGV[$f]) or die;
    my $sent_count = 0;
    while (<TEXT>) {
        chomp;
        my @items = split / /, $_;
        $form[$sent_count][$f] = [];
        foreach my $item (@items) {
            push $form[$sent_count][$f], $item;
        }
        $sent_count++;
    }
    close TEXT;
}

my %alignment_word;

foreach my $s (0 .. $#form) {
    my @alignment;
    my %candidate_scores;
    foreach my $w0 (0 .. $#{$form[$s][0]}) {
        foreach my $w1 (0 .. $#{$form[$s][1]}) {
            my $jarowinkler = Text::JaroWinkler::strcmp95( lc($form[$s][0][$w0]), lc($form[$s][1][$w1]), 20 ) - 0.6;
            $jarowinkler = 0 if $jarowinkler < 0;
            my $relpos0 = $#{$form[$s][0]} ? $w0/$#{$form[$s][0]} : 0.5;
            my $relpos1 = $#{$form[$s][1]} ? $w1/$#{$form[$s][1]} : 0.5;
            my $relpos = 1 - abs($relpos0 - $relpos1);
            $candidate_scores{"$w0-$w1"} = $jarowinkler * 8 + $relpos * 3;
        }
    }
    if ($type eq 'intersection') {
        my @sorted_candidates = sort{$candidate_scores{$b} <=> $candidate_scores{$a}} keys %candidate_scores;
        my $links_to_do = min($#{$form[$s][0]}, $#{$form[$s][1]}) + 1;
        my @used;
        foreach my $c (@sorted_candidates) {
            last if $candidate_scores{$c} < 4; 
            my ($w0, $w1) = split /-/, $c;
            if (!$used[0][$w0] && !$used[1][$w1]) {
                push @alignment, $c;
                $links_to_do--;
                $used[0][$w0] = 1;
                $used[1][$w1] = 1;
                $alignment_word{$form[$s][0][$w0]}{$form[$s][1][$w1]}++;
            }
            last if !$links_to_do;
        }
    }
    print join " ", @alignment;
    print "\n";
}

my $ALIGNED_WORDS = 1;
{
    open my $file, '>:utf8', $ARGV[2];
    foreach my $w0 (keys %alignment_word) {
        my @sorted = sort {$alignment_word{$w0}{$b} <=> $alignment_word{$w0}{$a}}
            keys $alignment_word{$w0};
        my $total = 0;
        foreach my $w1 (@sorted) {
            $total += $alignment_word{$w0}{$w1};
        }
        for (my $i = 0; $i < $ALIGNED_WORDS; $i++) {
            my $w1 = $sorted[$i];
            my $score = $alignment_word{$w0}{$w1} / $total;
            print $file "$w0 $w1 $score\n";
        }
    }
    close $file;
}


