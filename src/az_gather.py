import os
import time
import json
import datetime
import numpy as np
import cv2
from az_code import *
from az_farmer import *
from az_imaging import *
import pyscreenshot as ImageGrab
from PIL import ImageOps
from numpy import *
from pynput.mouse import Controller
from az_cord_helper import CordHelper
import logging

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/gather.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()

trs_x = 70
trs_y = 100
trs_w = 1470
trs_h = 927

wood_screen = (1425, 147, 1465, 163	)
stone_screen = (1425, 174 , 1465, 190)
straw_screen = (1425, 200 , 1465, 217)
food_screen = (1200, 116, 1238, 130)
apple_img = '/opt/dev/az/templates/gather/apple_vm_fb.png'
carrots_img = '/opt/dev/az/templates/gather/carrots_vm_fb.png'
#frame is [0, 0, 40, 16]

class Gather():
	def __init__(self):
		wood = self.get_stat(wood_screen, 'wood')
		stone = self.get_stat(stone_screen, 'stone')
		straw = self.get_stat(straw_screen, 'straw')
		food = self.get_stat(food_screen, 'food')
		self.wood = wood[0]
		self.wood_max = wood[1]
		self.stone = stone[0]
		self.stone_max = stone[1]
		self.straw =  straw[0]
		self.straw_max = straw[1]
		self.food = food[0]
		self.food_max = food[1]


	def get_stat(self, screen, tag):
		segment_grab_custom(screen, tag)
		out = get_num_from_image('segment_{}.jpg'.format(tag))
		print(out)
		try:
			curr, maxx = out.split('/')
			print("******** {} is : {} out of {}".format(tag, curr, maxx))
			return (int(curr), int(maxx))
		except:
			print("Didn't find /")


	def update_food(self):
		food = self.get_stat(food_screen, 'food')
		self.food = food[0]
		self.food_max = food[1]


	def img_exists(self, img, screen, method=cv2.TM_CCOEFF_NORMED, threshold=0.85):
		img = cv2.imread(img)
		screen = cv2.imread(screen)
		try:
			result = cv2.matchTemplate(screen, img, method)
			fres = np.where(result >= threshold)
			if len(fres[0])>0 and len(fres[1])>0:
				slots = zip(fres[0], fres[1])
				slot_set = set(slots)
				return list(slot_set)[0]
			else:
				return False
		except:
			raise Exception("Input images faulty!")


	def get_apples(self, zone):
		try:
			self.update_food() # get the latest food
		except:
			print("Couldn't get food, waiting...")
		if self.food >= 6:
			navy(zone, 3)
			segment_grab_color(trs_x, trs_y, trs_w, trs_h, True)
			cord = self.img_exists(apple_img, 'segment_color.png')
			if type(cord) == tuple:
				cord = ((cord[1]+trs_x+5, cord[0]+trs_y+5))
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				print("Cleared Apple Tree!")
				refresh_checker()
				self.get_apples(zone)
			else:
				print("No Apple Trees, moving on")
		else:
			print("Current food: {} too low".format(self.food))
			return


	def get_carrots(self, zone):
		try:
			self.update_food() # get the latest food
		except:
			print("Couldn't get food, waiting...")
		if self.food >= 6:
			navy(zone, 3)
			segment_grab_color(trs_x, trs_y, trs_w, trs_h, True)
			cord = self.img_exists(carrots_img, 'segment_color.png')
			if type(cord) == tuple:
				cord = ((cord[1]+trs_x+5, cord[0]+trs_y+5))
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				move_and_click((cord[0], cord[1]), 1)
				time.sleep(2)
				print("Cleared Carrots Field!")
				refresh_checker()
				self.get_apples(zone)
			else:
				print("No Carrot fields, moving on")
		else:
			print("Current food: {} too low".format(self.food))
			return


	def gather_apples(self):
		refresh_checker()
		self.get_apples('top_right')
		refresh_checker()
		self.get_apples('bottom_right')
		refresh_checker()
		self.get_apples('top_left')
		refresh_checker()		
		self.get_apples('bottom_left')


	def gather_carrots(self):
		refresh_checker()
		self.get_carrots('top_right')
		refresh_checker()
		self.get_carrots('bottom_right')
		refresh_checker()
		self.get_carrots('top_left')
		refresh_checker()
		self.get_carrots('bottom_left')


	def gatherer(self):
		self.gather_apples()
		self.gather_carrots()


if __name__ == '__main__':
	g = Gather()
	g.gatherer()