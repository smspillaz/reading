#!/bin/bash -x

git status --untracked-files=all --porcelain | grep "??" | grep papers/ | grep ".png" | cut -d ' ' -f 2 | xargs -L1 -I{} mv {} img/
