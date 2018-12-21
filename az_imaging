from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime
from az_code import *
from PIL import *
from PIL import ImageOps
from numpy import *
from pytesseract import image_to_string

#player_strength_loc = (2009, 136, 2049, 155)
#{'y': 136, 'x': 2009}


current_resources = {
	"strength": 0,
	"current_food": 0,
	"total_food": 0,
	"sesterti": 0,
	"helmets": 0,
	"rp": 0
}

def get_image(cords):
	box = cords
	im = ImageGrab.grab(box)
 	return im	


def get_player_stat(file_name, stat, num):
	data = load_file(file_name)
	cords = (data[stat]['x'], data[stat]['y'], data[stat]['x']+data[stat]['width'], data[stat]['y']+data[stat]['height'])
	im = get_image(cords)
	output_string = image_to_string(im, config='--psm 7')
	#im.save('eng.comic.exp' + str(num) + '.png', dpi=(116,116))
	print output_string
	return output_string


def food_split():
	data = get_player_stat('player.json', 'food', 1)
	data = data.split('/')
	return data

def upgrade_current_resources(timer):
	time.sleep(timer)
	current_resources['strength'] = int(get_player_stat('player.json', 'player_strength_loc', 0))
	time.sleep(timer)
	food = food_split()
	current_resources['current_food'] = food[0]
	current_resources['total_food'] = food[1]
	time.sleep(timer)
	current_resources['sesterti'] = int(get_player_stat('player.json', 'sesterti', 2))
	time.sleep(timer)
	current_resources['rp'] = int(get_player_stat('player.json', 'rp', 3))
	time.sleep(timer)
	current_resources['helmets'] = int(get_player_stat('player.json', 'helmets', 4))
	print current_resources
	return current_resources

if __name__ == '__main__':
	upgrade_current_resources(0.1)
	#output_cords()

#x1, y1, x2, y2
