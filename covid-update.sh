#!/bin/env bash
python3 nytimes_covid.py -getdata
commitMessage="$(grep 'Most Recent Update:' head.md | sed -e 's/\*//g' -e 's/*: //')"
echo "$commitMessage"

git add .
git commit -m "Berkshire County COVID update: $commitMessage"
git push -u origin master
