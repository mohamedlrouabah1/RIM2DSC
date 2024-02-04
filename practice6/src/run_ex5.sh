#!/usr/bin/bash

# In order to tune the BM25 weighting function, generate runs exploring the 2-dimensions space of its parameters
# (k1 and b). Think about your optimization strategy. A simple one could be to fix k1 to 1.2 and try 11 values for
# b (from 0.0 to 1.0, step = 0.1), and then fix b to 0.75 and try 21 values for k1 (from 0 to 4, step = 0.2)


queries_file=../queries.csv

echo "Param b: "
for b in $(LANG=en_EN seq 0.0 0.1 1.0 )
do
    python3 main_interactive.py -r bm25 --stopword -b "$b" "${queries_file}"
done
echo "done\n"

echo "Param k1: "
for k in $(LANG=en_EN seq 0.0 0.1 1.0 )
do
    python3 main_interactive.py -r bm25 --stopword --k1 "$k" "${queries_file}"
done
echo "done\n"
