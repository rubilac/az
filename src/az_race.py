import os
import sys
import time
import json
import datetime
from az_code import *
from az_farmer import *
import pyscreenshot as ImageGrab
from PIL import ImageOps
from PIL import Image
from numpy import *
import pynput.mouse as ms
import pynput.keyboard as kb
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
import numpy as np
import cv2
import shutil
import logging
import toml
config = toml.load('.config')


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


race_icon = config['race']['race_img']
five_mile_img = config['race']['five_mile_img']
ten_mile_img = config['race']['ten_mile_img']
twenty_mile_img = config['race']['twenty_mile_img']
miles_list = [five_mile_img, ten_mile_img, twenty_mile_img]

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
		#self.get_image()
		self.method = cv2.TM_CCOEFF_NORMED
		self.threshold = 0.95
		self.screen_x = 70
		self.screen_y = 160
		self.screen_w = 1488
		self.screen_h = 925
		self.img_path = '/opt/dev/az/templates/race/'
		self.race_box = '/opt/dev/az/templates/race_box.png'
		self.race_box_pos = (117, 342)
		self.race_pos = (920, 552)
		self.new_task_pos = (775, 691)
		self.task_1 = (602, 560)
		self.task_2 = (778, 560)
		self.task_3 = (968, 560)
		self.go_pos = (926, 687)
		self.dbl_miles_pos = (670, 609)
		self.single_miles_pos = (883, 607)
		self.close = (1022, 381)
		self.close_events = (1053, 371)


	def get_color_image(self, x, y, width, length, tag="default", save=True):
		"""
			Given x, y cords and width and length size, take a color image and return the summed value
			of all 3 rgb ints.
			Option to save the image is off by default.
		"""
		box = (x, y, x+width, y+length)
		im = ImageGrab.grab(box)
		fn = "race_colour_{}.png".format(tag)
		im.save(fn,'PNG')
		logger.info("Saved image: {}".format(fn))


	def is_race_ready(self):
		""" 
			return False if we find race_box.png
		"""
		template = cv2.imread(race_icon)
		self.get_color_image(70, 290, 100, 100, 'icon', True)
		screen = cv2.imread('race_colour_icon.png')
		try:
			result = cv2.matchTemplate(screen, template, self.method)
			fres = np.where(result >= self.threshold)
			if len(fres[0]) >= 1:
				print("Race Active!")
				return True
		except:
			print("Race is not Available! Try again later")
			return False


	def race(self):
		race = self.is_race_ready()
		if race:
			print("Clicking Race box")
			move_and_click(self.race_box_pos, 1)
			move_and_click(self.race_pos, 1)
			move_and_click(self.new_task_pos, 1)
			at = self.available_tasks()
		else:
			print("No race available.")


	def available_tasks(self):
		#[(607, 486), (787, 489), (785, 486), (603, 494), (966, 494), (960, 493), (960, 492), (605, 494), (960, 491), (786, 486), (604, 494), (608, 489), (784, 494), (783, 494), (606, 486)]
		slot_1 = 680
		slot_2 = 860
		slot_1_holder = 0
		slot_2_holder = 0
		slot_3_holder = 0
		x, y, h, w = (475, 365, 600, 350)
		screen = self.get_color_image(x, y, h, w, 'default')
		im=np.array(Image.open("race_colour_default.png").convert('RGB'))
		sought = [179, 236, 139]
		fres = np.where(np.all(im==sought,axis=2))
		slots = list(set(zip(fres[1]+x, fres[0]+y)))
		for slot_x, slot_y in slots:
			if slot_x < slot_1 and slot_1_holder == 0:
				slot_1_holder = 1
			elif slot_1 < slot_x < slot_2 and slot_2_holder == 0:
				slot_2_holder = 1
			elif slot_2 < slot_x and slot_3_holder == 0:
				slot_3_holder = 1
			else:
				pass
		out_list = [slot_1_holder, slot_2_holder, slot_3_holder] # return array with 0 or 1 if task is acceptable
		self.get_miles("race_colour_default.png", out_list)


	def bonus_miles(self):
		x, y, h, w = (699, 502, 40, 20)
		screen = self.get_color_image(x, y, h, w, 'bonus_miles')
		im=np.array(Image.open("race_colour_bonus_miles.png").convert('RGB'))
		sought = [179, 236, 139]
		fres = np.where(np.all(im==sought,axis=2))
		if len(fres[0]) > 0:
			move_and_click(self.dbl_miles_pos, 1)
		else:
			print("Not enough carrots or apples, farm more!")
			return


	def get_miles(self, screen, at_list):
		# at_list = [1, 0, 1]
		slot_1 = 680
		slot_2 = 860
		slot_1_holder = 0
		slot_2_holder = 0
		slot_3_holder = 0
		screen = cv2.imread(screen)
		out = []
		for i in miles_list:
			result = cv2.matchTemplate(screen, cv2.imread(i), self.method)
			fres = np.where(result >= self.threshold)
			if len(fres[0]) > 0:
				out_x = fres[1]+475
				miles = int(i.split('/')[-1].split('_')[0])
				if out_x < slot_1:
					slot_1_holder = 5
				elif slot_1 < out_x < slot_2:
					slot_2_holder = 10
				elif slot_2 < out_x:
					slot_3_holder = 20
				else:
					print("sad")
			else:
				pass
		out = [slot_1_holder, slot_2_holder, slot_3_holder]
		self.get_best_task(at_list, out)


	def get_best_task(self, at_list, mile_list):
		tsl_1 = (609, 546)
		tsl_2 = (774, 537)
		tsl_3 = (952, 542)
		tsl = [tsl_1, tsl_2, tsl_3]
		in_l = list(set(zip(at_list, mile_list)))
		index = 0
		best_slot = (0, 0)
		for x, y in in_l:
			if x == 1 and y > best_slot[1]:
				best_slot = (index, y)
			index += 1
		print(best_slot)
		move_and_click(tsl[best_slot[0]], 1)
		move_and_click(self.go_pos, 1)
		self.bonus_miles()
		move_and_click(self.close, 1)
		move_and_click(self.close_events, 1)





if __name__ == '__main__':
	race = Race()
	race.race()