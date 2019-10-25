#!/bin/bash
ps -ef | grep runner.sh | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep az_combat.py | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep az_farmer.py | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep az_crafting.py | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep az_gather.py | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep az_inv.py | grep -v grep | awk '{print $2}' | xargs kill