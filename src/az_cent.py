import os
import time
import json
from datetime import datetime
import numpy as np
import cv2
from az_code import *
from az_farmer import *
import pyscreenshot as ImageGrab
from PIL import ImageOps
from numpy import *
from pynput.mouse import Controller
from az_cord_helper import CordHelper
import logging
import toml
from az_imaging import ImageLoader

config = toml.load('.config')
method =  cv2.TM_CCOEFF_NORMED

orange_colours = [[251, 79, 82], [253, 85, 85], [254, 86, 85], [251, 84, 85],[242, 76, 75], [159, 217, 169], [210, 169, 167], [254, 72, 3], [244, 96, 8], [253, 88, 3], [220, 92 ,17], [247, 92, 0], [223, 102, 0], [230, 117, 14], [238, 109, 1], [237, 109, 0], [237, 109, 0], [237, 108, 0], [237, 106, 1], [236, 106, 0]]


def list_test(l1):
	l2 = orange_colours
	for i in l1:
		if i in l2:
			print(i)
		else:
			pass


def flatten(listo):
	out = []
	for i in listo:
		for x in i:
			out.append(x)
	return out


def curr_time():
	now = datetime.datetime.now()
	current_time = now.strftime("%y%m%d%H%M%S")
	return current_time


def print_colours_from_img(img):
	out = cv2.imread(img)
	print(out.tolist())


def unique_list_of_list(inlist):
	out = []
	for i in inlist:
		if i in out:
			pass
		else:
			out.append(i)
	print(out)


class LaunchCent():
	def __init__(self):
		move_and_click((780, 369), 1)
		self.stop_pos = (981, 692)
		self.map_box = (790, 620, 830, 670)
		self.angle_box = (851, 554, 908, 601)
		self.power_box = (1016, 642, 1044, 649)
		self.stone_powerup = (561, 698)
		self.target_box = (820, 435, 823, 440)


	def scan_space_for_colour(self, colour_list, box, ts=False):
		seg = self.get_screen_segment(box, ts)
		for px in colour_list:
			if px in seg:
				print("Found Orange using {}".format(px))
				return True
			else:
				pass
		return False


	def scan_img_for_colour(self, colour_list, img):
		seg = flatten(np.array((cv2.imread(img))).tolist())
		flatt = flatten(colour_list)
		for px in flatt:
			if px in seg:
				print("Found Orange using {} - Click Stop NOW!".format(px))
				return True
			else:
				pass
		print("Didn't find colour!")
		return False


	def scanner(self, box, timer=0, ts=False):
		scan = self.scan_space_for_colour(orange_colours, box, ts)
		mousePos(self.stop_pos, 1)
		while scan == False:
			scan = self.scan_space_for_colour(orange_colours, box, ts)
		time.sleep(timer)
		quick_click(self.stop_pos, 0)


	def punch_coordinator(self):
		self.scanner(self.map_box)
		move_and_click(self.stop_pos, 1)
		time.sleep(2)
		self.scanner(self.angle_box)
		time.sleep(2)
		self.scanner(self.power_box, 0.85)
		move_and_click(self.stone_powerup, 1)
		time.sleep(7)
		self.scanner(self.target_box)


	def get_screen_segment(self, box, ts=False):
		x, y, w, h = box
		img = ImageGrab.grab(bbox=(x, y, w, h))
		segment = np.array(img)
		#cv2.namedWindow("main", cv2.WINDOW_NORMAL)
		#cv2.imshow('main', cv2.cvtColor(np.array(segment), cv2.COLOR_BGR2RGB))
		#ct = curr_time()
		#fn = "aa_tmp_{}.png".format(ct)
		#img.save(fn,'PNG')
		if cv2.waitKey(25) & 0xFF==ord('q'):
			cv2.destroyAllWindows()
			sys.exit()
		flat_out = flatten(segment.tolist())
		if ts:
			print(flat_out)
		return flat_out


if __name__ == '__main__':
	l = LaunchCent()
	l.punch_coordinator()
