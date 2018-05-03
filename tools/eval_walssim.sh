mkdir walssim_eval

for N in 1 2 3 5 10 22
do
    echo $N-best > walssim_eval/$N
    for l in `cat langs_tgt`
    do
        tools/eval_srcsel.py -N $N delex_uas_las/$l.las walssim/$l.iso
    done >> walssim_eval/$N
done

echo > walssim_eval/0
cat langs_tgt >> walssim_eval/0

# TODO sorted...
paste walssim_eval/* > walssim_eval.tsv
rm -r walssim_eval

