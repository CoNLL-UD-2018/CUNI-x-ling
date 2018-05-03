#!/bin/bash
#
# Print each command to STDERR before executing (expanded), prefixed by "+ "
set -o xtrace

s=cs
t=en

R=`pwd`
mkdir hunwork/$s-$t
cd hunwork/$s-$t
$R/partialAlign.py $R/watchtower/sentences/$s.s $R/watchtower/sentences/$t.s split $s $t > batch
$R/hunalign -bisent -utf $R/empty -batch batch

