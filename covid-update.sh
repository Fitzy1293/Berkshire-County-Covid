#!/bin/env bash

function run {
    date > run_date
    python3 nytimes_covid.py -getdata

    git add .  &&
    git commit -m "Berkshire County COVID update: $(date)" &&
    git push origin "$(git status | head -n 1 | sed 's/.* //')"


}
run &&  
while true; do

run
sleep 6h


done
