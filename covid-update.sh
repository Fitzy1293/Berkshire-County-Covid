#!/bin/env bash
python3 nytimes_covid.py -getdata
commitMessage="$(grep "COVID Update:" head.md | sed 's/\*//g')"
echo "$commitMessage"

git add .
git commit -m "Berkshire County COVID update: $commitMessage"
git push -u origin master
