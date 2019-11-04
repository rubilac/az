#!/bin/bash
echo `date` + " -- Starting Runner.sh" >> runs.log

for (( ; ; ))
do
   #sudo rm -rf /var/log/kern.log.*
   echo `date` >> runs.log
   python3 az_combat.py
   python3 az_farmer.py
   python3 az_crafting.py
   #python3 az_gather.py
   python3 az_inv.py
   python3 az_race.py
done