#! /bin/bash

pyinstaller --add-data 'tcss/:tcss' -F main.py -n llf
