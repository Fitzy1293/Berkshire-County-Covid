#!/bin/env bash

function run {
    date > run_date
    python3 nytimes_covid.py -getdata

    git add COVID_plots.png All_Berkshire_Data_Provided.csv README.md &&
    git commit -m "Berkshire County COVID update: $(date)" &&
    git push origin "$(git status | head -n 1 | sed 's/.* //')"
}

run &&
while true; do

run
sleep 6h


done
