#!/bin/bash
function run {
        python3 nytimes_covid.py
        commitMessage="$(grep 'Most Recent Update:' head.md | sed -e 's/\*//g' -e 's/Most Recent Update: //')"
        git add .
        git commit -m "Berkshire County COVID update: $commitMessage"
        git push -u origin "$(git status | head -n 1 | sed 's/.* //')"
}
while true; do
    date > run_date
    run
    sleep 1s
done
