#!/bin/bash

echo "starting"
echo "input string" $1
python test.py <<eof
$1
eof
