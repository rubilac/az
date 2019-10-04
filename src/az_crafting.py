import os
import time
import json
import datetime
import numpy as np
import cv2
from az_code_mac import *
from az_farmer_mac import *
from PIL import ImageGrab
from PIL import ImageOps
from numpy import *
from pynput.mouse import Controller
from az_cord_helper import CordHelper
import logging

mouse = pynput.mouse.Controller()

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/crafting.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()


method =  cv2.TM_CCOEFF_NORMED
craft_pos = (-244, 669)
close_pos = (-139, 216)
first_pos = (-587, 291)
stone_mason_pos = (-668, 321)
stone_mason_build = (-585, 307)
carpenter_pos = (-458, 320)
carpenter_build = (-364, 327)
blacksmith_pos = (-328, 383)
tailor_pos = (-837, 549)
leatherworker_pos = (-705, 495)
blank_spot = (-974, 242)

class Craft():
	def __init__(self):
		self.town_x = 185*2
		self.town_y = 316*2
		self.town_w = 885*2
		self.town_h = 551*2
		print("Crafting Module Engaged!")
		nav_to_town()


	def collect(self, building):
		""" Collect from building """
		secure_click(building, anchor, 1)


	def collect_all(self):
		secure_click(stone_mason_pos, anchor, 1)
		secure_click(carpenter_pos, anchor, 1)
		secure_click(blacksmith_pos, anchor, 1)
		secure_click(tailor_pos, anchor, 1)
		secure_click(leatherworker_pos, anchor, 1)


	def craft_stone(self):
		""" Craft stone """
		if self.building_state(stone_mason_pos) == 1:
			secure_click(stone_mason_pos, anchor, 1)
			secure_click(blank_spot, anchor, 1)
			secure_click(stone_mason_pos, anchor, 1)
			secure_click(stone_mason_build, anchor, 1) 
			secure_click(first_pos, anchor, 1)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(close_pos, anchor, 0.2)
			print("Crafting Stone Block")
		else:
			print("Stone Mason is busy, not crafting")


	def craft_wood_plank(self):
		""" Craft Planks """
		if self.building_state(carpenter_pos) == 1:
			secure_click(carpenter_pos, anchor, 1)
			secure_click(blank_spot, anchor, 1)
			secure_click(carpenter_pos, anchor, 1)
			secure_click(carpenter_build, anchor, 1) 
			secure_click(first_pos, anchor, 1)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(craft_pos, anchor, 0.2)
			secure_click(close_pos, anchor, 0.2)
			print("Crafting Wood Plank")
		else:
			print("Stone Mason is busy, not crafting")


	def building_state(self, building):
		# {'x': 185, 'y': 316}
		# {'x': 1070, 'y': 827}
		""" 
			returns 0 if working
			returns 1 if available
		"""
		secure_mouse_over(building, anchor, 1) # mouseover building
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h) # screengrab town
		self.ready_state = is_ready()
		return self.ready_state



if __name__ == '__main__':
	anchor = get_anchor()
	get_anchored_cursor(anchor)
	crafter = Craft()
	crafter.craft_stone()
	crafter.craft_wood_plank()
	#crafter.building_state(stone_mason_pos)

