#!/bin/env bash

function run {

    python3 nytimes_covid.py -getdata

    git add COVID_plots.png All_Berkshire_Data_Provided.csv README.md run_date &&
    git commit -m "Berkshire County COVID update: $(date)" &&
    git push origin "$(git status | head -n 1 | sed 's/.* //')"
}


while true; do

date > run_date && run && sleep 6h


done
