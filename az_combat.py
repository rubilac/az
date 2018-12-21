from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime
from az_code import *
from PIL import ImageOps
from numpy import *

"""
Modules:
	Am I fighting fit?
		> 40 current strength
	Validate enemy exists from list
		Ignore if absent
		Engage if present
	Defeat Enemy
		Enemy Strength

"""

enemy_exists_int = 510



def check_enemy_exists(file_name, ind, location):
	data = load_file(file_name)
	navy(location, 1)
	enemies = data['sequence']['loc'][0]['enemies']
	for i in range(len(enemies)):
		if data['sequence']['loc'][0]['enemies'][i]['index'] == ind:
			enemy = data['sequence']['loc'][0]['enemies'][ind-1]
			enemy_cords = (enemy['cord']['x'], enemy['cord']['y'])
			box = (enemy['cord']['x'], enemy['cord']['y']-38, enemy['cord']['x']+50, enemy['cord']['y']-30 )
			mousePos(enemy_cords)
			time.sleep(1)
			im = ImageOps.grayscale(ImageGrab.grab(box))
			a = array(im.getcolors())
			a = a.sum()
			if a == enemy_exists_int:
				print "Oh crap theres a baddie here!~!!"
				return True
			else:
				return False


def enemy_roll_check(file_name):
	alive_enemies = []
	data = load_file(file_name)
	locations = data['sequence']['loc']
	for loc in locations:
		enemies = data['sequence']['loc'][locations.index(loc)]['enemies']
		for enemy in enemies:
			enemy_index = enemy['index']
			enemy_loc = enemy['loc']
			if check_enemy_exists(file_name, enemy_index, enemy_loc):
				alive_enemies.append(enemy_index)
			else:
				print "No enemy with index {} found".format(enemy_index)
	print alive_enemies
	return alive_enemies


def fight(target):
	if enemy_exists ==
	mousePos(target)



if __name__ == '__main__':
	#get_player_strength(unit_1)
	#check_enemy_exists('enemies.json',9)
	enemy_roll_check('enemies.json')
	#output_cords()
