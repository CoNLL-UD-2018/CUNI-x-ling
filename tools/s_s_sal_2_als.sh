
for s in `cat langs`
do
    for t in `cat langs`
    do
        if [ -e sentence_alignments/$s-$t.watchtower.sal ]
        then
            echo $s-$t
            ./s_s_sal_2_als.py sentences/$s.s sentences/$t.s sentence_alignments/$s-$t.watchtower.sal \
                > parallel_sentences/$s-$t.als &
        fi
    done
done

