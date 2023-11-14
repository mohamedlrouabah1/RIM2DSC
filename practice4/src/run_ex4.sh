#!/usr/bin/bash

queries_file=../queries.csv

weighting_functions=(
    'smart_ltc' 
    'smart_ltn'
    'bm25'
)

stopwords=(
    ''
    '-s'
)

stemmer=(
    None
    porter
)

for weighting_function in "${weighting_functions[@]}"
do
    for stopword in "${stopwords[@]}"
    do
        for stemmer in "${stemmer[@]}"
        do
            python3 main.py -r $weighting_function $stopword  -m $stemmer "${queries_file}"
        done
    done
done