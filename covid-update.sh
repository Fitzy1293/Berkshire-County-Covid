#!/bin/env bash

commitMessage="$(date +'%m/%d/%Y' | sed 's#/#-#g')"

git add .
git commit -m "Berkshire County COVID update: ${commit}"
git push -u origin master
