import os
import time
import json
import datetime
import numpy as np
import cv2
from az_code import *
from az_farmer import *
from az_imaging import *
from az_crafting import Craft
import pyscreenshot as ImageGrab
from PIL import ImageOps
from numpy import *
from pynput.mouse import Controller
from az_cord_helper import CordHelper
import logging

# chrome position - (134, 70, 1654, 891)
# 0 134  138  1417 858

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/gather.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()

trs_x = 70
trs_y = 160
trs_w = 1488
trs_h = 925

wood_screen = (1440, 148, 1465, 162	)
wood_max_screen = (1445, 148, 1465, 162)
straw_screen = (1440, 235 , 1475, 250)
stone_screen = (1440, 202 , 1465, 216)
food_screen = (1211, 175, 1248, 188)
apple_img = '/opt/dev/az/templates/gather/apple_vm_fb.png'
carrots_img = '/opt/dev/az/templates/gather/carrots_vm_fb.png'
straw_img = '/opt/dev/az/templates/gather/straw_vm_fb.png'
#frame is [0, 0, 40, 16]

class Gather():
	def __init__(self):
		#wood = self.get_stat(wood_screen, 'wood')
		#stone = self.get_stat(stone_screen, 'stone')
		#straw = self.get_stat(straw_screen, 'straw')
		food = self.get_stat(food_screen, 'food')
		#self.wood = wood[0]
		#self.wood_max = self.get_max(wood_max_screen, 'wood_max')
		#self.stone = stone[0]
		#self.stone_max = stone[1]
		#self.straw =  straw[0]
		#self.straw_max = straw[1]
		#self.food = food[0]
		#self.food_max = food[1]
		pass


	def get_max(self, screen, tag):
		segment_grab_custom(screen, tag)
		out = get_num_from_image('segment_{}.jpg'.format(tag))
		print(out)
		return out

	def get_stat(self, screen, tag):
		segment_grab_custom(screen, tag)
		out = get_num_from_image('segment_{}.jpg'.format(tag))
		try:
			curr, maxx = out.split('/')
			print("******** {} is : {} out of {}".format(tag, curr, maxx))
			return (int(curr), int(maxx))
		except:
			test = int(out)
			if type(test) == int:
				maxx = int(out.split()[0][-2:])
				curr = int(out.split()[0][:-2])
				print("******** {} is : {} out of {}".format(tag, curr, maxx))
				return (curr, maxx)
			else:
				print("Didn't find /,  {}".format(out))
				return False


	def update_food(self):
		try:
			food = self.get_stat(food_screen, 'food')
			self.food = food[0]
			self.food_max = food[1]
		except:
			self.food = 0
			print("reading failed")
			return False

	def update_straw(self):
		try:
			straw = self.get_stat(straw_screen, 'straw')
			self.straw = straw[0]
			self.straw_max = straw[1]
		except:
			print("reading failed")
			return False

	def img_exists(self, img, screen, method=cv2.TM_CCOEFF_NORMED, threshold=0.80):
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
					time.sleep(15)
					print("Cleared Apple Tree!")
					refresh_checker()
					self.get_apples(zone)
				else:
					print("No Apple Trees, moving on")
					return
			else:
				print("Current food: {} too low".format(self.food))
				return
		except:
			print("Couldn't get food, waiting...")
			return


	def get_carrots(self, zone):
		try:
			self.update_food() # get the latest food
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
					time.sleep(15)
					print("Cleared Carrots Field!")
					refresh_checker()
					self.get_carrots(zone)
				else:
					print("No Carrot fields, moving on")
			else:
				print("Current food: {} too low".format(self.food))
				return
		except:
			print("Couldn't get food, waiting...")


	def get_straw(self, zone):
		try:
			self.update_straw()
			self.update_food() # get the latest food
			if self.straw < self.straw_max-15 and self.food >= 15:
				navy(zone, 3)
				segment_grab_color(trs_x, trs_y, trs_w, trs_h, True)
				cord = self.img_exists(straw_img, 'segment_color.png')
				if type(cord) == tuple:
					cord = ((cord[1]+trs_x+10, cord[0]+trs_y+10))
					n = 15
					while n > 0:
						move_and_click((cord[0], cord[1]), 1)
						n -= 1
					time.sleep(15)
					print("Cleared Straw Patch!")
					refresh_checker()
					self.get_straw(zone)
				else:
					print("No Straw Patches, moving on")
					return
			else:
				print("Current food: {} too low".format(self.food))
				print("Current straw: {} too high".format(self.straw))
				return
		except:
			print("Couldn't get straw, try again later...")
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


	def gather_straw(self):
		az_map = ['top_right', 'bottom_right', 'top_left', 'bottom_left']
		self.update_straw()
		if self.straw > self.straw_max-15:
			craft = Craft()
			craft.craft_flax()
			straw_tmp = self.straw
			self.update_straw()
			if self.straw >= straw_tmp:
				print("Couldn't craft flax, stopping")
				return
			else:
				for zone in az_map:
					refresh_checker()
					self.get_straw(zone)
		else:
			for zone in az_map:
				refresh_checker()
				self.get_straw(zone)



	def gatherer(self):
		self.gather_straw()
		self.gather_apples()
		self.gather_carrots()
		


if __name__ == '__main__':
	#segment_grab_color(trs_x, trs_y, trs_w, trs_h, True)
	zoom_out()
	g = Gather()
	g.gatherer()