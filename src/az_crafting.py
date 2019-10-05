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


def get_anchor():
    """ Get the cords of the anchor """
    threshold = 0.99
    segment = cv2.imread("segment.png", cv2.IMREAD_GRAYSCALE)
    try:
        template = cv2.imread("/opt/dev/az/templates/anchor.png", cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(segment, template, method)
        fres = np.where(result >= threshold)
        cord = (int(fres[1]/2), int(fres[0]/2))
        print("Anchor Found @ : {}".format(cord))
        return cord
    except:
        template = cv2.imread("/opt/dev/az/templates/popup_anchor.png", cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(segment, template, method)
        fres = np.where(result >= threshold)
        cord = (int(fres[1]/2), int(fres[0]/2))
        print("Popup Anchor Found @ : {}".format(cord))
        return cord 


class Craft():
	def __init__(self):
		self.town_x = 185*2
		self.town_y = 316*2
		self.town_w = 885*2
		self.town_h = 551*2
		self.anchor = get_anchor()
		print("Crafting Module Engaged!")
		nav_to_town()


	def collect(self, building):
		""" Collect from building """
		secure_click(building,self.anchor, 1)


	def collect_all(self):
		secure_click(stone_mason_pos,self.anchor, 1)
		secure_click(carpenter_pos,self.anchor, 1)
		secure_click(blacksmith_pos,self.anchor, 1)
		secure_click(tailor_pos,self.anchor, 1)
		secure_click(leatherworker_pos,self.anchor, 1)


	def craft_stone(self):
		""" Craft stone """
		if self.building_state(stone_mason_pos) == 1:
			secure_click(stone_mason_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(stone_mason_pos,self.anchor, 1)
			secure_click(stone_mason_build,self.anchor, 1) 
			secure_click(first_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Stone Block")
		else:
			print("Stone Mason is busy, not crafting")


	def craft_wood_plank(self):
		""" Craft Planks """
		if self.building_state(carpenter_pos) == 1:
			secure_click(carpenter_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(carpenter_pos,self.anchor, 1)
			secure_click(carpenter_build,self.anchor, 1) 
			secure_click(first_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
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
		secure_mouse_over(building,self.anchor, 1) # mouseover building
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h) # screengrab town
		self.ready_state = is_ready()
		return self.ready_state

	def crafting(self):
		self.craft_stone()
		self.craft_wood_plank()

if __name__ == '__main__':
	crafter = Craft()
	crafter.crafting()


