from PIL import ImageGrab
import os
import time
#import win32api, win32con
import json
import datetime
from az_code_mac import *
from PIL import ImageOps
from numpy import *
from pynput.mouse import Button, Controller
from pytesseract import image_to_string

mouse = Controller()

inventory_check_int = 50185
inv_bx = 100
inv_by = 15

inv_1 = (200, 492, 310, 510)
inv_2 = (365, 492, 475, 510)
inv_3 = (530, 492, 640, 510)
inv_4 = (200, 671, 310, 690)
inv_5 = (365, 671, 475, 690)
inv_6 = (530, 671, 640, 690)

inv_slots = [inv_1, inv_2, inv_3, inv_4, inv_5, inv_6]
inv_before = 0
inv_next = 0
inv_close = 0
inv_beetroot = ("BEEeTROoTS", "beetroots")
inv_boar_skins = ("b=70F eS ed", "boar_skins")
inv_boar_tooth = ("Boar TOOTH", "boar_tooth")
inv_centurions = ("feta iT ite) 4", "centurions")
inv_chickens = ("fetta ti)","chickens")
inv_crabs = ("Crass", "crabs")

inv_list = [inv_beetroot, inv_boar_skins, inv_boar_tooth, inv_centurions, inv_chickens, inv_crabs]

def open_bag():
	move_and_click((787,1091))


def open_bag_check():
	box = (inv_1[0]*2, inv_1[1]*2, inv_1[2]*2, inv_1[3]*2)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	a = array(im.getcolors())
	a = a.sum()
	#print(a)
	#im.save("inventory.png",'PNG')
	if a == inventory_check_int:
		print("Inventory is open")
	else:
		print("Inventory not open, opening inventory")
		open_bag()
		#open_bag_check()


def get_image(x, y, width, length):
	box = (x, y, width, length)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	im.save("{}-{}-{}-{}.png".format(x, y, width, length),'PNG')
	a = array(im.getcolors())
	a = a.sum()
	print(a)
	#print(a.sum())


def convert_to_string(im):
	os = image_to_string(im, config='--psm 6')
	print(os)
	return os


def find_inv_name(inp):
	for k,v in inv_list:
		if k == inp:
			print(v)
			return v
	print("no match")


def get_inv_slots(inv_slots):
	counter = 0
	for i_s in inv_slots:
		counter += 1
		box = (i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2)
		im = ImageOps.grayscale(ImageGrab.grab(box))
		im.save("inv_slot_{}.png".format(counter),'PNG')
		os = image_to_string(im, config='--psm 6')
		data = find_inv_name(os)


if __name__ == '__main__':
	get_inv_slots(inv_slots)
	#get_image(inv_1[0]*2, inv_1[1]*2, inv_1[2]*2, inv_1[3]*2)
	#get_image(668, 534, 800, 600)
	#open_bag_check()
	#output_cords()
	#mousePos((300, 480))