from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime
from az_code import *
from PIL import ImageOps
from numpy import *

boar_exist_int = [324, 325, 419, 578, 672, 562, 988, 1571]

def boar_exists(cords):
	""" return true if on mouse-over at cord a boar hover is observed"""
	x = cords[0]
	y = cords[1]
	box = (x, y-30, x+30, y-25 )
	left_box = (x-80, y, x-50, y+5 )
	mousePos((x,y))
	time.sleep(1)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	a = array(im.getcolors())
	a = a.sum()
	im.save('test.png', dpi=(116,116))
	bm = ImageOps.grayscale(ImageGrab.grab(left_box))
	bm.save('left_test.png', dpi=(116,116))
	b = array(bm.getcolors())
	b = b.sum()
	print a, b
	for i in boar_exist_int:
		if i in [a, b]:
			print("OMG BOAR HERE, GET EM!")
			#print a, b
			return True
	return False

def spawner(file_name, location, hunt_type):
    """return a list of tuples given a sequence file
    [[(), (), (), ()], [(), (), (), ()]]
    """
    sequence = load_file(file_name)
    spawns = []
    loc = sequence['sequence']['loc']
    n = len(loc)-1
    while n >= 0:
        n -= 1
        if loc[n]['name'] == location:
            if hunt_type == 'fish':
                spawn_inc = loc[n][hunt_type][0]['spawns']
                spawn_len = len(spawn_inc)-1
                spawns = []
                while spawn_len >= 0:
                    spawns_temp = (spawn_inc[spawn_len]['x'], spawn_inc[spawn_len]['y'])
                    spawns.append(spawns_temp)
                    spawn_len -= 1
                return spawns
            elif hunt_type == 'boars':
                boar_spawns = []
                for i in range(len(loc[n][hunt_type])):
                    data = loc[n][hunt_type][i]['spawns']
                    data_len = len(data)-1
                    spawns = []
                    while data_len >= 0:
                        spawns_temp = (data[data_len]['x'], data[data_len]['y'])
                        spawns.append(spawns_temp)
                        data_len -= 1
                    boar_spawns.append(spawns)
                return boar_spawns


def get_start_point(file_name, location, hunt_type, ind):
    sequence = load_file(file_name)
    nav_list = sequence['sequence']['loc']
    for i in nav_list:
        if i['name'] == location:
            ret_loc = (i[hunt_type][ind]['start_point']['x'], i[hunt_type][ind]['start_point']['y'])
            return ret_loc


def farmer(file_name, location, hunt_type, timer=2.5):
    time.sleep(2)
    cord_list = spawner(file_name, location, hunt_type)
    navy(location)
    time.sleep(2)
    if hunt_type == 'fish':
        print("{} : Fishing started @ {}".format(datetime.datetime.now(),location))
        move_and_click(get_start_point(file_name, location, hunt_type, 0),5)
        for i in cord_list:
			if boar_exists(i):
				move_and_click(i, timer)
			else:
				print("Move along, no fish here... continuing to next cord")
    else:
        print("Gimme dem Boars!")
        time.sleep(2)
        if type(cord_list[0]) != list:
        	n = 3
        	while n > 0:
				print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
				#move_and_click(get_start_point(file_name, location, hunt_type, 0),5)
				for i in cord_list:
					if boar_exists(i):
						move_and_click(i, timer)
					else:
						print("Move along, no boar here... continuing to next cord")
				n -= 1
        else:
            for i in range(len(cord_list)):
            	n = 3
            	while n > 0:
            	 	print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
	                #move_and_click(get_start_point(file_name, location, hunt_type, i),5)
	                for x in cord_list[i]:
						if boar_exists(x):
							move_and_click(x, timer)
						else:
							print("Move along, no boar here... continuing to next cord")
	            	n -= 1

    
def does_boar_exist_cursor():
	data = output_cords()
	cord = (data['x'], data['y'])
	boar_exists(cord)


def cycle():
	navy('bottom_right')
	move_and_click(get_start_point('simple.json', 'bottom_right', 'boars', 0),10)
	#farmer('simple.json', 'bottom_right', 'boars', 5)
	farmer('simple.json', 'bottom_right', 'fish', 10)
	navy('bottom_left')
	move_and_click(get_start_point('simple.json', 'bottom_left', 'boars', 0),10)
	#farmer('simple.json', 'bottom_left', 'boars', 5)
	farmer('simple.json', 'bottom_left', 'fish', 10)
	navy('top_right')
	move_and_click(get_start_point('simple.json', 'top_right', 'fish', 0),10)
	farmer('simple.json', 'top_right', 'fish', 10)


if __name__ == '__main__':
	#while True:
	cycle()
   	#farmer('simple.json', 'bottom_left', 'boars', 5)
   	#cord = (1028, 1342)
   	#boar_exists(cord)
   	#does_boar_exist_cursor()