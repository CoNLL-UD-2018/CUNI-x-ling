#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use autodie;
use PerlIO::gzip;
use List::Util "max";

sub say {
    my $line = shift;
    print "$line\n";
}

sub tsvsay {
    my $line = join "\t", @_;
    print "$line\n";
}

binmode STDIN, ':utf8';
binmode STDOUT, ':utf8';
binmode STDERR, ':utf8';

{
    # I want my arguments to be UTF-8
    use I18N::Langinfo qw(langinfo CODESET);
    use Encode qw(decode);
    my $codeset = langinfo(CODESET);
    @ARGV = map { decode $codeset, $_ } @ARGV;
}

if ( @ARGV != 0 ) {
    die("Usage: $0 \n");
}

sub process {
    my ($line) = @_;

    chomp $line;
    my ($words_str, $alignments_str, $probs_str) = split /  # /, $line;
    
    my @words = split / /, $words_str;
    $words[0] = 'NULL';
    
    my @alignments = map { $_ } (split / /, $alignments_str);
    unshift @alignments, 0;

    my @probs;
    if (defined $probs_str) {
        @probs = map { $_ } (split / /, $probs_str);
        unshift @probs, 0;
    }

    return (\@words, \@alignments, \@probs);
}

sub spaces {
    my ($n, $c) = @_;

    $c = defined $c ? $c : ' ';

    foreach my $i (1..$n) {
        print $c;
    }

    return ;
}

sub print_cs {
    my ($cs, $no, $max_en_len) = @_;

    print $no;
    spaces($max_en_len+1-length($no));
    say (join ' ', @$cs);

    return ;
}

sub print_en {
    my ($en, $en_al, $en_index, $max_en_len, $cs, $cs_al, $cs_probs) = @_;

    my $c = ($en_index+1)%3 ? ' ' : '.';
    my $en_word = $en->[$en_index];
    print $en_word;
    spaces($max_en_len-length($en_word));

    foreach my $cs_index (0..$#$cs) {
        my $cc = ($en_index+1)%3 && ($cs_index+1)%2 ? ' ' : '.';
        print $cc;
        my $aligned_en = 0;
        my $aligned_cs = 0;
        if ($en_al->[$en_index] == $cs_index) {
            $aligned_en = 1;
        }
        if ($cs_al->[$cs_index] == $en_index) {
            $aligned_cs = 1;
        }

        my $cs_len = length($cs->[$cs_index]);
        if ($aligned_cs || $aligned_en) {
            my $spaces_1 = max(0, int($cs_len/2)-1);
            spaces($spaces_1, $c);
            if ($aligned_cs) {
                if ($aligned_en) {
                    print @$cs_probs ? int(10*$cs_probs->[$cs_index]) : '+';
                } else {
                    print '|';
                }
            } else {
                print '—';
            }
            spaces($cs_len-$spaces_1-1, $c);
        } else {
            spaces($cs_len, $c);
        }

    }
    
    print "\n";

    return ;
}

my $no = 1;
while (<>) {
    my $csline = <>;
    my $enline = <>;
    my ($cs, $cs_al, $cs_probs) = process($csline);
    my ($en, $en_al, $en_probs) = process($enline);
    
    foreach my $en_index (0..$#$en) {
        my $aligned_cs = $en_al->[$en_index];
        my $aligned_en = $cs_al->[$aligned_cs];
        if ($aligned_en == $en_index && $aligned_en != 0 && $aligned_cs != 0) {
            # TODO and $en_probs->[$en_index] > $THRESHOLD
            tsvsay($en->[$aligned_en], $cs->[$aligned_cs]);
        }
    }
}


