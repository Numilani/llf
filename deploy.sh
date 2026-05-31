#! /bin/bash

pyinstaller --add-data 'tcss/:tcss' -F main.py -n llf
cp dist/llf ~/.local/bin
