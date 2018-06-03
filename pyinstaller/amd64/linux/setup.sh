#!/bin/bash
cp ../../../src/*.py $PWD/.
cp ../../../src/amd64/*.so $PWD/.
$HOME/.local/bin/pyinstaller -F --add-data cryptonight.so:. -p $PWD xmr-miner.py
read -p "Press ENTER to continue..." key
