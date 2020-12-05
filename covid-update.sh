#!/bin/bash
python3 nytimes_covid.py -getdata
commitMessage="$(grep 'Most Recent Update:' head.md | sed -e 's/\*//g' -e 's/Most Recent Update: //')"
date +%s > last_run_UTC
echo "$commitMessage"

git add .
git commit -m "Berkshire County COVID update: $commitMessage"
git push origin master
