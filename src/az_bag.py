from PIL import ImageGrab
import os
import sys
import time
import json
import datetime
from az_code_mac import *
from PIL import ImageOps
from numpy import *
from pynput.mouse import Button, Controller
from pytesseract import image_to_string
import numpy as np
import cv2
from az_farmer_mac import *
import shutil

mouse = Controller()

inventory_check_int = 50185
x = 250
y = 550
inv_bx = 100
inv_by = 100
iyd = 179
ixd = 165
inv_1 = (x, y, x+inv_bx, y+inv_by)
inv_2 = (x+ixd, y, x+ixd+inv_bx, y+inv_by)
inv_3 = (x+ixd+ixd, y, x+ixd+ixd+inv_bx, y+inv_by)
inv_4 = (x, y+iyd, x+inv_bx, y+iyd+inv_by)
inv_5 = (x+ixd, y+iyd, x+ixd+inv_bx, y+iyd+inv_by)
inv_6 = (x+ixd+ixd, y+iyd, x+ixd+ixd+inv_bx, y+iyd+inv_by)

inv_def = {
			"item_name" : "replace_me",
			"item_int" : 0,
			"item_max" : 100,
			"item_count_cur" : 0,
			"item_count_prev" : 0,
			"item_delete" :	False,
			"item_stacksize" : 5
		}


def open_bag():
	w = 2200
	h = 2200
	method = cv2.TM_CCOEFF_NORMED
	threshold = 0.99
	segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1,1,w,h)))
	template = cv2.imread('../templates/inventory/inventory_icon.png', cv2.IMREAD_GRAYSCALE)
	ps = np.array(segment.getdata(), dtype='uint8').reshape((segment.size[0], segment.size[1],-1))
	result = cv2.matchTemplate(ps, template, method)
	fres = np.where(result >= threshold)
	print(fres)
	try:
		cord = (int(fres[1]/2+5), int(fres[0]/2+5))
		print("Found Inventory Button @ {}, openning inventory".format(cord))
		move_and_click(cord)
	except TypeError:
		print("Cannot find inventory button, quitting...")
		sys.exit()	


def show_frame():
	w = 2400
	h = 2400
	f = 0.5
	wx = w*f
	hx = w*f

	segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1,1,w,h)))
	ps = np.array(segment.getdata(), dtype='uint8').reshape((segment.size[0], segment.size[1],-1))
	regulated = cv2.resize(ps, (0,0), fx=f, fy=f)
	#method = cv2.TM_CCOEFF_NORMED
	#threshold = 0.99
	#template = cv2.imread('inventory.png', cv2.IMREAD_GRAYSCALE)
	#result = cv2.matchTemplate(ps, template, method)
	#fres = np.where(result >= threshold)
	#print(fres, int(fres[0]), int(fres[1]))
	#mousePos((int(fres[1]*f),int(fres[0]*f)))

	cv2.namedWindow('window', 0)
	cv2.resizeWindow('window', int(wx), int(hx))
	cv2.imshow('window', regulated)
	wait = True
	while wait:
		wait = cv2.waitKey() == 'q113'


def show_image():
	template = cv2.imread('../templates/inventory/inventory_icon.png', cv2.IMREAD_GRAYSCALE)
	cv2.namedWindow('window', 0)
	cv2.imshow('window', template)
	wait = True
	while wait:
		wait = cv2.waitKey() == 'q113'


def reset_counter(file_name):
	""" Copy the current counter to previous, and reset the current counter """
	items = load_file(file_name)
	for item in items['il']:
		item['item_count_prev'] = item['item_count_cur']
		item['item_count_cur'] = 0
	with open('../fixtures/items.json', 'w') as outfile:
	    json.dump(items, outfile, indent=4, sort_keys=True)	


def open_bag_check():
	# Get screen, find inventory.pn in screen. return the inventory cords 
	w = 2200
	h = 2200
	method = cv2.TM_CCOEFF_NORMED
	threshold = 0.99
	segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1,1,w,h)))
	template = cv2.imread('../templates/inventory/inventory.png', cv2.IMREAD_GRAYSCALE)
	ps = np.array(segment.getdata(), dtype='uint8').reshape((segment.size[0], segment.size[1],-1))
	result = cv2.matchTemplate(ps, template, method)
	fres = np.where(result >= threshold)
	try:
		cord = (int(fres[1]/2), int(fres[0]/2))
		print("Inventory is open @ {}".format(cord))
		return cord
	except TypeError:
		print("Inventory is not open, trying to open bag.")


def get_image(x, y, width, length, tag="default"):
	box = (x, y, width, length)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	im.save("inv{}.png".format(tag),'PNG')
	a = array(im.getcolors())
	a = a.sum()
	print(a)
	return int(a)


def get_color_image(x, y, width, length, tag="default"):
	box = (x, y, width, length)
	im = ImageGrab.grab(box)
	im.save("inv{}.png".format(tag),'PNG')
	arr = np.asarray(im)
	tot = arr.sum(0).sum(0)
	result = tot.sum()
	print(result)
	return int(result)


def add_item_to_store(item_int):
	items = load_file("../fixtures/items.json")
	new_inv = inv_def
	new_inv['item_int'] = item_int
	items['il'].append(new_inv)
	with open('../fixtures/items.json', 'w') as outfile:
	    json.dump(items, outfile, indent=4, sort_keys=True)


def update_item_count(item_int):
	items = load_file("../fixtures/items.json")
	count = 0
	for item in items["il"]:
		if item["item_int"] == int(item_int):
			#print("Updating {} with 1".format(item_int))
			items['il'][count]["item_count_cur"] += 1
			with open('../fixtures/items.json', 'w') as outfile:
			    json.dump(items, outfile, indent=4, sort_keys=True)
			break
		count += 1


def img_in_store(item_int):
	items = load_file("../fixtures/items.json")
	try:
		item_detail = list(filter(lambda x: x['item_int'] == item_int, items['il']))
		update_item_count(item_int)
		#print(dict(item_detail[0]))
		return dict(item_detail[0])
	except IndexError:
		print("Item_int not found, adding item to store with default values, please populate data")
		add_item_to_store(item_int)
		img_in_store(item_int) 
	

def get_inv_slots(bag_cord):
	inv_slots = inv_slot_gen(bag_cord)
	counter = 0
	for i_s in inv_slots:
		counter += 1
		img = get_color_image(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2, counter)
		if img == 32705332 or img == 21902624:
			print("End of inventory, exitting!")
			sys.exit()
		else: 
			img_in_store(img)


def inv_slot_gen(inv_cord):
	""" Given the inventory coordinate, return the coords for each inventory slot """
	x = inv_cord[0]-135
	y = inv_cord[1]+102
	inv_bx = 100
	inv_by = 100
	iyd = 179
	ixd = 165
	inv_1 = (x, y, x+inv_bx, y+inv_by)
	inv_2 = (x+ixd, y, x+ixd+inv_bx, y+inv_by)
	inv_3 = (x+ixd+ixd, y, x+ixd+ixd+inv_bx, y+inv_by)
	inv_4 = (x, y+iyd, x+inv_bx, y+iyd+inv_by)
	inv_5 = (x+ixd, y+iyd, x+ixd+inv_bx, y+iyd+inv_by)
	inv_6 = (x+ixd+ixd, y+iyd, x+ixd+ixd+inv_bx, y+iyd+inv_by)
	inv_slots = inv_slots = [inv_1, inv_2, inv_3, inv_4, inv_5, inv_6]
	return inv_slots


def inv_slot_sell_gen(slot_cord, slot):
	""" Given the slot coordinate, return the coords for each slots sell button """
	sx = slot_cord[0]+75
	sy = slot_cord[1]+110
	cord = (sx, sy)
	return cord


def inv_nav_left(bag_cord):
	left_cord = (bag_cord[0]-200, bag_cord[1]+250)
	move_and_click(left_cord)


def inv_nav_right(bag_cord):
	right_cord = (bag_cord[0]+350, bag_cord[1]+250)
	move_and_click(right_cord)


def read_inv_slots(inv_slots):
	counter = 0
	for i_s in inv_slots:
		counter += 1
		img = get_image(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2, counter)


def refresh_inventory():
	#Focus frame
	move_and_click((450, 240))
	cord = open_bag_check()
	reset_counter("../fixtures/items.json")
	bag_number = 1
	while True:
		print("Bag Number: {}".format(bag_number))
		get_inv_slots(cord)
		inv_nav_right(cord)
		bag_number += 1


del_list = [31311194, 29946229, 35747789, 34398448, 32002882, 34490115, 34898008, 32887210, 34455958, 29758269] #icicles, snowballs, fish, twisted_branch


def bag_cleaner(del_list, bag_cord=0, bypass=False):
	""" 	"""	
	if bypass == False:
		try:
			bag_cord = open_bag_check()
			inv_slots = inv_slot_gen(bag_cord)
			delete(inv_slots, bag_cord)
		except TypeError:
			print("Inventory is not open, trying to open bag.")
			open_bag() # fix the problem and restart the function
			bag_cord = open_bag_check()
			return bag_cleaner(del_list, bag_cord, True)
	else:
		inv_slots = inv_slot_gen(bag_cord)
		delete(inv_slots, bag_cord)


def delete(inv_slots, bag_cord):
	counter = 0
	for i_s in inv_slots:
		img = get_color_image(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2, counter)
		if img == 32705332 or img == 21902624:
			print("End of inventory, exitting!")
			sys.exit()
		elif img in del_list: 
			print("Found Item to delete, deleting...")
			delete_item(bag_cord, img, counter) # delete the item and restart the function
			return bag_cleaner(del_list, bag_cord, True)
		else:
			print("Nothing to delete here!")
		counter += 1


def delete_item(bag_cord, item_int, slot):
	""" Given an item_int, find the item_int inv_slot on the page and execute the delete sequence """
	mbx = bag_cord[0]
	mby = bag_cord[1]+300
	minus = (mbx, mby)
	confirm_sell = (bag_cord[0]+80, bag_cord[1]+370)
	all_slots = inv_slot_gen(bag_cord)
	tar_slot = all_slots[slot]
	x, y, bx, by = tar_slot
	sell_button = inv_slot_sell_gen((x, y), xddslot)
	mousePos(sell_button)
	move_and_click(sell_button)
	time.sleep(1)
	mousePos(minus)
	move_and_click(minus)
	time.sleep(1)
	mousePos(confirm_sell)
	move_and_click(confirm_sell)
	time.sleep(1)
	move_and_click((450, 240))


def cleanup_loop(bag_cord):
	bag_number = 1
	print(bag_cord)
	while True:
		print("Cleaning Bag Number: {}".format(bag_number))
		bag_cleaner(bag_cord)
		inv_nav_right(bag_cord)
		bag_number += 1


def cleanup_inventory():
	#Focus frame
	move_and_click((450, 240))
	try:
		bag_cord = open_bag_check()
		cleanup_loop(bag_cord)
	except:
		open_bag()
		return cleanup_inventory()


def save_inventory_to_file(new_file):
	#refresh_inventory() #Refresh the inventory
	shutil.copyfile('../fixtures/items.json', new_file)

	
def location_finder(dx=0):
	#take picture @ loc
	x_range = [400, 410]
	y_range = [500, 510]
	amph = 28775496
	counter=0
	cord = open_bag_check()
	inv_slots = (inv_slot_gen(cord))
	x, y, w, h = inv_slots[0]
	print(inv_slots[0], x, y, w, h)
	get_color_image(x*2, y*2, w*2, h*2, 's1')


def build_slots(x_r, y_r):
	""" 
	400, 500 
	410, 510
	405, 505
	"""
	w = 100
	h = 100
	big_range = []
	x_s, x_e = x_r
	y_s, y_e = y_r
	x_diff = x_e - x_s
	y_diff = y_e - y_s
	print(x_diff, y_diff)
	for x in range(x_diff+1):
		for y in range(y_diff+1):
			cord = ((x_s+x)*2, (y_s+y)*2, (x_s+x+w)*2, (y_s+y+h)*2)
			big_range.append(cord)
	print(big_range)
	return big_range

def find_cord(cord_range):

	for cord in cord_range:
		x, y, w, h = cord
		if get_color_image(x, y, w, h, 's1') == 28775496:
			print("finally found it fuck yeah")
			break
		else:
			continue


def grav_inv():
	pass


if __name__ == '__main__':
	#cleanup_inventory()
	#refresh_inventory()
	#save_inventory_to_file('items_arty.json')
	#location_finder(5)
	#c_r = build_slots([390, 410], [530, 550])
	#find_cord(c_r)
	get_color_image(808, 1094, 1008, 1294,'s2')