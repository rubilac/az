#!/bin/bash

for (( ; ; ))
do
   echo date > runs.log
   python3 az_combat_mac.py
   python3 az_farmer_mac.py
   python3 az_crafting.py
   python3 inv_backup.py
done