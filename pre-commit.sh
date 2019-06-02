#!/bin/bash
pip install black fiximports

for file in ./src/*
do
    if [[ -f $file ]]; then
        fiximports $file
    fi
done

black .
tox