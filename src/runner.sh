#!/bin/bash

for (( ; ; ))
do
   echo `date` > runs.log
   python3 az_farmer.py
   python3 az_combat.py
   python3 az_crafting.py
done