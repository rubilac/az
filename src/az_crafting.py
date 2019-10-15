import os
import time
import json
import datetime
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

mouse = pynput.mouse.Controller()

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/crafting.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()


method =  cv2.TM_CCOEFF_NORMED
craft_pos = (876, 707)
blank_spot = (341, 373)
close_pos = (960, 345)


# Crafting Positions
first_pos = (564, 415)
second_pos = (533, 477)
third_pos = (513, 544)
fourth_pos = (518, 610)
fifth_pos = (513, 678)

# Stone Mason
stone_mason_pos = (528, 440)
stone_mason_build = (595, 435)

# Carpenter
carpenter_pos = (698, 449)
carpenter_build = (775, 454)

# Blacksmith
blacksmith_pos = (802, 496)
blacksmith_build = (874, 504)

# Tailor
tailor_pos = (396, 631)
tailor_build = (457, 630)

#Merchandise info
merch_pos_1 = (734, 480)
merch_pos_2 = (863, 479)
merch_pos_3 = (728, 620)
close_merch_pos = (943, 390)
close_merch_pos_2 = (877, 416)

#Fish Market
fish_market_pos = (625, 621)
fish_market_build = (639, 682)
fish_market_restock = (688, 613)
fish_market_img = '/opt/dev/az/templates/fish_soup_2.png'
fish_soup_img = '/opt/dev/az/templates/inventory/items/fish_soup_single_2.png'

#Butcher
butcher_pos = (715, 667)
butcher_build = (740, 741)
butcher_restock = (787, 673)
butcher_img = '/opt/dev/az/templates/gaul_soup.png'
gaul_soup_img = '/opt/dev/az/templates/inventory/items/gaul_soup_single_2.png'



#Leatherworker
leatherworker_pos = (496, 583)
leatherworker_build = (567, 582)



class Craft():
	def __init__(self):
		self.town_x = 185
		self.town_y = 316
		self.town_w = 885
		self.town_h = 551
		self.sell_cord_list = [(-668, 382), (-509, 395), (-342, 383), (-664, 543), (-503, 550), (-344, 560)]
		print("Crafting Module Engaged!")
		refresh_checker()
		nav_to_town()


	def collect(self, building):
		""" Collect from building """
		move_and_click(building, 1)


	def collect_all(self):
		move_and_click(stone_mason_pos, 1)
		move_and_click(carpenter_pos, 1)
		move_and_click(blacksmith_pos, 1)
		move_and_click(tailor_pos, 1)
		move_and_click(leatherworker_pos, 1)


	def get_image(self, x=1, y=1, width=1250, length=920, save=True):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageOps.grayscale(ImageGrab.grab(box))
		if save:
			fn = "tmp_merch_stock.png"
			im.save(fn,'PNG')
			params = ['mogrify', fn, fn]
			subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
			logger.info("Saved image: {}".format(fn))
		a = array(im.getcolors())
		a = a.sum()
		logger.info("Got grayscale image: {}".format(a))
		return int(a)


	def building_state(self, building):
		# {'x': 185, 'y': 316}
		# {'x': 1070, 'y': 827}
		""" 
			returns 0 if working
			returns 1 if available
		"""
		mousePos(building, 1) # mouseover building
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h) # screengrab town
		self.ready_state = is_ready()
		return self.ready_state


	def craft_stone(self):
		""" Craft stone """
		if self.building_state(stone_mason_pos) == 1:
			move_and_click(stone_mason_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(stone_mason_pos, 1)
			move_and_click(stone_mason_build, 1) 
			move_and_click(first_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Stone Block")
		else:
			print("Stone Mason is busy, not crafting")


	def craft_wood_plank(self):
		""" Craft Planks """
		if self.building_state(carpenter_pos) == 1:
			move_and_click(carpenter_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(carpenter_pos, 1)
			move_and_click(carpenter_build, 1) 
			move_and_click(first_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Wood Plank")
		else:
			print("Carpenter is busy, not crafting")


	def craft_fish_soup(self):
		""" Craft Fish Soup """
		if self.building_state(fish_market_pos) == 1:
			move_and_click(fish_market_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(fish_market_pos, 1)
			move_and_click(fish_market_build, 1) 
			move_and_click(second_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Fish Soup")
		else:
			print("Fish Market is busy, not crafting")


	def craft_iron_bar(self):
		""" Craft Bar """
		if self.building_state(blacksmith_pos) == 1:
			move_and_click(blacksmith_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(blacksmith_pos, 1)
			move_and_click(blacksmith_build, 1) 
			move_and_click(first_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Iron Bar")
		else:
			print("Blacksmith is busy, not crafting")


	def craft_nails(self):
		""" Craft Bar """
		if self.building_state(blacksmith_pos) == 1:
			move_and_click(blacksmith_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(blacksmith_pos, 1)
			move_and_click(blacksmith_build, 1) 
			move_and_click(fourth_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Nails")
		else:
			print("Blacksmith is busy, not crafting")


	def craft_gaul_soup(self):
		""" Craft Gaul Soup """
		if self.building_state(butcher_pos) == 1:
			move_and_click(butcher_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(butcher_pos, 1)
			move_and_click(butcher_build, 1) 
			move_and_click(first_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Gaul Soup")
		else:
			print("Butcher is busy, not crafting")


	def craft_leather(self):
		""" Craft Gaul Soup """
		if self.building_state(leatherworker_pos) == 1:
			move_and_click(leatherworker_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(leatherworker_pos, 1)
			move_and_click(leatherworker_build, 1) 
			move_and_click(first_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Leather")
		else:
			print("Leatherworker is busy, not crafting")


	def craft_grease(self):
		""" Craft Gaul Soup """
		if self.building_state(leatherworker_pos) == 1:
			move_and_click(leatherworker_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(leatherworker_pos, 1)
			move_and_click(leatherworker_build, 1) 
			move_and_click(fourth_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Grease")
		else:
			print("Leatherworker is busy, not crafting")


	def restock_state(self, building, img_path):
		# mouseover building
		# take snapper
		# if merch exists return false
		# otherwise return true
		secure_mouse_over(building, 3) # mouseover building
		time.sleep(3)
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h) # screengrab town
		self.ready_state = ready_custom(img_path)
		return self.ready_state


	def get_merch_slot(self, cord):
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
		if cord[0] < 1250 and cord[1] < 900:
			out = [self.sell_cord_list[0]]
			return out
		if cord[0] < 1250 and 900 < cord[1] < 1200:
			out = [self.sell_cord_list[1]]
			return out
		if cord[0] < 1250 and cord[1] > 1200:
			out = [self.sell_cord_list[2]]
			return out
		if cord[0] > 1250 and cord[1] < 900:
			out = [self.sell_cord_list[3]]
			return out
		if cord[0] > 1250 and 900 < cord[1] < 1200:
			out = [self.sell_cord_list[4]]
			return out
		if cord[0] > 1250 and cord[1] > 1200:
			out = [self.sell_cord_list[5]]
			return out


	def load_stock(self, item_name, img_path, pos):
		move_and_click(pos, 1) # Click Merch pos, this will open up inventory frame
		self.get_image() # Get inventory frame
		screen = cv2.imread('tmp_merch_stock.png') # LOad our inv frame from pvs
		template = cv2.imread(img_path) # Load our item we want to stock
		try:
			result = cv2.matchTemplate(screen, template, method) # Does it match?
			fres = np.where(result >= 0.99)
			if fres[0].size == 0:
				print("Couldn't match {} in open slot".format(item_name))
				return 1
			cord = (int(fres[0]), int(fres[1]))
			click_cord = self.get_merch_slot(cord)[0]
			print("Found {} @ {} in slot {}".format(item_name, cord, click_cord))
			move_and_click(click_cord, 1)
			print("Loading {} in slot {}".format(item_name, pos))
		except:
			print("No {} found! Make some!".format(item_name))
			return 1


	def town_grab(self):
		# pas
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h)


	def load_stock_slots(self, stock, img_path):
		self.load_stock(stock, img_path, merch_pos_1)
		self.load_stock(stock, img_path, merch_pos_2)
		self.load_stock(stock, img_path, merch_pos_3)
		move_and_click(close_merch_pos, 1)


	def restock_fish_market(self):
		if self.restock_state(fish_market_pos, fish_market_img) == 1:
			print("Restocking Fish Market")
			move_and_click(fish_market_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(fish_market_pos, 1)
			move_and_click(fish_market_restock, 1)
			self.load_stock_slots('fish_soup', fish_soup_img)
			move_and_click(close_merch_pos, 1)
		else:
			print("Fish market full!")


	def restock_butcher(self):
		if self.restock_state(butcher_pos, butcher_img) == 1:
			print("Restocking Butcher!")
			move_and_click(butcher_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(butcher_pos, 1)
			move_and_click(butcher_restock, 1)
			self.load_stock_slots('gaul_soup', gaul_soup_img)
			move_and_click(close_merch_pos, 1)
		else:
			print("Butcher full!")


	def craft(self):
		self.craft_stone() # Stone Mason
		self.craft_wood_plank() # Carpenter
		self.craft_iron_bar() # Blacksmith
		self.craft_leather() # Leatherworker
		self.craft_gaul_soup() # Butcher
		self.craft_fish_soup() # Fish Market


	def restock(self):
		self.restock_fish_market()
		self.restock_butcher()



if __name__ == '__main__':
	crafter = Craft()
	crafter.craft()
	#crafter.restock()

