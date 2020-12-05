#!/bin/env bash

commitMessage="$(date +'%m/%d/%Y' | sed 's#/#-#g')"

git add .
git commit -m "Berkshire County COVID update: $commitMessage"
git push -u origin master
echo "Commit message: $commitMessage"
