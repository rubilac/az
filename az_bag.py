from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime
from az_code import *
from PIL import ImageOps
from numpy import *

'''
	box = (x, y-30, x+30, y-25 )
	left_box = (x-80, y, x-50, y+5 )
	mousePos((x,y))
	time.sleep(1)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	a = array(im.getcolors())
	a = a.sum()
	im.save('test.png', dpi=(116,116))
'''

inventory_check_int = 35866
inv_1
inv_2
inv_3
inv_4
inv_5
inv_6
inv_before
inv_next
inv_close


def open_bag():
	move_and_click((2192,1264))


def open_bag_check():
	box = (1058, 516, 1206, 547)
	im = ImageOps.grayscale(ImageGrab.grab(box))
	a = array(im.getcolors())
	a = a.sum()
	if a == inventory_check_int:
		print("Inventory is open")
	else:
		print("Inventory not open, opening inventory")
		open_bag()
		open_bag_check()

if __name__ == '__main__':
	#output_cords()
	open_bag_check()