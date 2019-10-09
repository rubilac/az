import os
import sys
import time
import json
import datetime
from az_code_mac import *
from az_farmer_mac import *
from PIL import ImageGrab
from PIL import ImageOps
from numpy import *
import pynput.mouse as ms
import pynput.keyboard as kb
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
import numpy as np
import cv2
import shutil
import logging

# Globals #
pwd = os.path.realpath('..')
fixture_path = os.path.join(pwd, 'fixtures/')
anchor_img = '/opt/dev/az/templates/anchor.png'
inv_icon_img = '/opt/dev/az/templates/inventory/inventory_icon.png'
inv_img = '/opt/dev/az/templates/inventory/inventory.png'

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/inventory.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()

# Keyboard and Mouse Interacters #
mouse = ms.Controller()
key = kb.Controller()

def get_match_result(ps, template, method, threshold):
	result = cv2.matchTemplate(ps, template, method)
	fres = np.where(result >= threshold)
	if len(fres[0]) > 1:
		raise Exception("Too many values found in results, refine threshold")
	elif len(fres[0]) == 0:
		raise Exception("No values found in results please refine threshold")
	else:
		return fres


class Race():
	"""
		This class manages the inventory of a player and can:
		 - Output the inventory values to a json file
		 - Clean up the inventory from a list of unwanted items
		 - TODO: Update the database with current values
		 - TODO: Generate the delete list from ../fixtures/items.json
		 - This class is anchor aware and coordinates are related to the point of the anchor
	"""

	def __init__(self):
		# Store anchor point
		# Store Inventory points
		# Store Sell points
		print("Race Module engaged!")
		self.get_image()
		self.method = cv2.TM_CCOEFF_NORMED
		self.threshold = 0.95
		self.screen_x = 1
		self.screen_y = 1
		self.screen_w = 2400
		self.screen_h = 2400
		self.anchor = get_anchor()
		self.img_path = '/opt/dev/az/templates/race/'
		self.race_box = '/opt/dev/az/templates/race_box.png'
		self.race_box_pos = (-1055, 169)
		self.race_pos = (-338, 459)
		self.new_task_pos = (-510, 634)
		self.go_pos = (-326, 629)
		self.close = (-205, 244)


	def get_image(self, x=1, y=1, width=2400, length=2400, tag="default", save=False):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageOps.grayscale(ImageGrab.grab(box))
		#ts = int(time.time())
		if save:
			fn = "tmp_race-{}.png".format(tag)
			im.save(fn,'PNG')
			params = ['mogrify', fn, fn]
			subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
			logger.info("Saved image: {}".format(fn))
		a = array(im.getcolors())
		a = a.sum()
		logger.info("Got grayscale image: {}".format(a))
		return int(a)


	def get_color_image(self, x, y, width, length, tag="default", save=False):
		"""
			Given x, y cords and width and length size, take a color image and return the summed value
			of all 3 rgb ints.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageGrab.grab(box)
		ts = int(time.time())
		if save:
			fn = "colorimg{}-{}.png".format(tag, ts)
			im.save(fn,'PNG')
			logger.info("Saved image: {}".format(fn))
		arr = np.asarray(im)
		tot = arr.sum(0).sum(0)
		result = tot.sum()
		logger.info("Got color image: {}".format(result))
		return int(result)


	def load_image(self, img_path, img_name):
		img_full_path = '{}{}.png'.format(img_path, img_name) 
		img_tmp = cv2.imread(img_full_path)
		return img_tmp


	def race_quest_active(self):
		""" 
			return False if we find race_box.png
		"""
		template = self.load_image('/opt/dev/az/templates/','race_box.png')
		self.get_image(True)
		screen = self.load_image('','tmp_race-default.png')
		try:
			result = cv2.matchTemplate(screen, template, self.method)
			fres = np.where(result >= self.threshold)
			if len(fres[0]) >= 1:
				print("Race not active!")
				return False
		except:
			print("Race is available!")
			return True


	def race(self):
		race = self.race_quest_active()
		if race:
			print("Clicking Race box")
			secure_click(self.race_box_pos, self.anchor, 1)
			secure_click(self.race_pos, self.anchor, 1)
			secure_click(self.new_task_pos, self.anchor, 1)
			best_match = self.find_best_match()


	def find_best_match(self):
		pass

	def get_sell_button(self, cord):
		""" 
			cord = (1000, 2000) 
			pos1 = (<1200, <800)
			pos2 = (<1200, >800<1200)
			pos3 = (<1200, >1200)
			pos4 = (>1200, <800)
			pos5 = (>1200, >800<1200)
			pos6 = (>1200, >1200)

		"""
		sell_buttons = self.sell_cord_list
		if cord[0] < 1200 and cord[1] < 800:
			out = [1, self.sell_cord_list[0]]
			return out
		if cord[0] < 1200 and 800 < cord[1] < 1200:
			out = [2, self.sell_cord_list[1]]
			return out
		if cord[0] < 1200 and cord[1] > 1200:
			out = [3, self.sell_cord_list[2]]
			return out
		if cord[0] > 1200 and cord[1] < 800:
			out = [4, self.sell_cord_list[3]]
			return out
		if cord[0] > 1200 and 800 < cord[1] < 1200:
			out = [5, self.sell_cord_list[4]]
			return out
		if cord[0] > 1200 and cord[1] > 1200:
			out = [6, self.sell_cord_list[5]]
			return out



if __name__ == '__main__':
	segment_grab(trs_x, trs_y, trs_w, trs_h, True)
	race = Race()
	race.race()