#!/bin/bash

python3 main.py &
sleep 1s
cd visualisation
python3 visualisation.py & 