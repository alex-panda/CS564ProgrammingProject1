#!/bin/bash

if ! [ -x "$(command -v python)" ]; then

    if ! [ -x "$(command -v python3)" ]; then
        echo "python and python3 commands did not work!"
        exit 1
    fi
    python3 parser.py ebay_data/items-*.json
    exit 1
fi
python parser.py ebay_data/items-*.json
