#!/bin/bash
rm -f $PWD/xmr-miner-amd64/usr/local/bin/empty
cp ../dist/xmr-miner $PWD/xmr-miner-amd64/usr/local/bin/.
dpkg --build xmr-miner-amd64
read -p "Press ENTER to continue..." key
