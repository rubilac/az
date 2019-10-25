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
import toml
config = toml.load('.config')

mouse = pynput.mouse.Controller()

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/crafting.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()


method =  cv2.TM_CCOEFF_NORMED
craft_pos = (980, 686)
blank_spot = (484, 371) #(341, 373)
close_pos = (1072, 322)

# Crafting Positions
first_pos = (635, 398) # (564, 415)
second_pos = (648, 459) # (533, 477)
third_pos = (665, 522) # (513, 544)
fourth_pos = (653, 595) # (518, 610)
fifth_pos = (662, 660) # (513, 678)

# Stone Mason
stone_mason_pos = (735, 399)
stone_mason_build = (802, 392)

# Carpenter
carpenter_pos = (907, 409)
carpenter_build = (983, 411)

# Blacksmith
blacksmith_pos = (1012, 454)
blacksmith_build = (1081, 463)

# Tailor
tailor_pos = (611, 588)
tailor_build = (677, 584) # TBD

#Leatherworker
leatherworker_pos = (708, 538)
leatherworker_build = (786, 538)

#Merchandise info
merch_pos_1 = (836, 468)
merch_pos_2 = (964, 460)
merch_pos_3 = (828, 600)
close_merch_pos = (1050, 371)
close_merch_pos_2 = (983, 397)

#Fish Market
fish_market_pos = (837, 580)
fish_market_build = (856, 636)
fish_market_restock = (908, 569)
fish_market_img = '/opt/dev/az/templates/fish_soup_vm_fb.png'
fish_soup_img = '/opt/dev/az/templates/inventory/items/fish_soup_single_2.png'

#Butcher
butcher_pos = (927, 629)
butcher_build = (956, 699)
butcher_restock = (1006, 630)
butcher_img = '/opt/dev/az/templates/gaul_soup_vm_fb.png'
gaul_soup_img = '/opt/dev/az/templates/inventory/items/gaul_soup_single_2.png'


class Craft():
	def __init__(self):
		from az_farmer import town_grab, refresh_checker
		self.town_x = 442
		self.town_y = 200
		self.town_w = 800
		self.town_h = 450
		self.sell_cord_list = [(645, 460), (764, 460), (913, 460), (645, 600), (764, 600), (913, 600)]
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
		from az_farmer import town_grab, refresh_checker, is_ready
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


	def craft_milestone(self):
		""" Craft stone """
		buy_dye = (1018, 563)
		if self.building_state(stone_mason_pos) == 1:
			move_and_click(stone_mason_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(stone_mason_pos, 1)
			move_and_click(stone_mason_build, 1) 
			move_and_click(fourth_pos, 1)
			move_and_click(buy_dye, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(buy_dye, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(buy_dye, 1)
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

	def craft_flax(self):
		""" Craft Gaul Soup """
		if self.building_state(tailor_pos) == 1:
			move_and_click(tailor_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(tailor_pos, 1)
			move_and_click(tailor_build, 1) 
			move_and_click(fifth_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Flax")
		else:
			print("Tailor is busy, not crafting")



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
		x1 = 650
		x2 = 800
		y = 500
		sell_buttons = self.sell_cord_list
		if cord[0] < y and cord[1] < x1:
			out = [self.sell_cord_list[0]]
			return out
		if cord[0] < y and x1 < cord[1] < x2:
			out = [self.sell_cord_list[1]]
			return out
		if cord[0] < y and cord[1] > x2:
			out = [self.sell_cord_list[2]]
			return out
		if cord[0] > y and cord[1] < x1:
			out = [self.sell_cord_list[3]]
			return out
		if cord[0] > y and x1 < cord[1] < x2:
			out = [self.sell_cord_list[4]]
			return out
		if cord[0] > y and cord[1] > x2:
			out = [self.sell_cord_list[5]]
			return out


	def load_stock(self, item_name, img_path, pos):
		move_and_click(pos, 1) # Click Merch pos, this will open up inventory frame
		self.get_image() # Get inventory frame
		screen = cv2.imread('tmp_merch_stock.png') # LOad our inv frame from pvs
		template = cv2.imread(img_path) # Load our item we want to stock
		try:
			result = cv2.matchTemplate(screen, template, method) # Does it match?
			fres = np.where(result >= 0.90)
			if fres[0].size == 0:
				print("Couldn't match {} in open slot".format(item_name))
				return 1
			elif fres[0].size > 1:
				cord = (int(fres[0][0]), int(fres[1][0]))
			else:
				cord = (int(fres[0]), int(fres[1]))
			click_cord = self.get_merch_slot(cord)[0]
			print("Found {} @ {} in slot {}".format(item_name, cord, click_cord))
			move_and_click(click_cord, 1)
			print("Loading {} in slot {}".format(item_name, pos))
		except:
			print("No {} found! Make some!".format(item_name))
			return 1


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
		ccfg = config['crafting']
		print(ccfg)

		#stone mason
		if ccfg['stone_mason'] == 'stone':
			self.craft_stone()
		elif ccfg['stone_mason'] == 'milestone':
			self.craft_milestone()
		elif ccfg['stone_mason'] == 0:
			print('Skipping stone_mason crafting')
		else:
			print('I dont know how to do that at the stone_mason')

		#carpenter
		if ccfg['carpenter'] == 'wooden_plank':
			self.craft_wood_plank()
		elif ccfg['carpenter'] == 0:
			print('Skipping carpenter crafting')
		else:
			print('I dont know how to do that at the carpenter')

		#blacksmith
		if ccfg['blacksmith'] == 'nails':
			self.craft_nails()
		elif ccfg['blacksmith'] == 'iron_bar':
			self.craft_iron_bar()
		elif ccfg['blacksmith'] == 0:
			print('Skipping blacksmith crafting')
		else:
			print('I dont know how to do that at the blacksmith')

		#leatherworker
		if ccfg['leatherworker'] == 'leather':
			self.craft_leather()
		elif ccfg['leatherworker'] == 'grease':
			self.craft_grease()
		elif ccfg['leatherworker'] == 0:
			print('Skipping leatherworker crafting')
		else:
			print('I dont know how to do that at the leatherworker')

		#tailor
		if ccfg['tailor'] == 'flax':
			self.craft_flax()
		elif ccfg['tailor'] == 0:
			print('Skipping tailor crafting')
		else:
			print('I dont know how to do that at the tailor')

		#fish_market
		if ccfg['fish_market'] == 'fish_soup':
			self.craft_fish_soup()
		elif ccfg['fish_market'] == 0:
			print('Skipping fish_market crafting')
		else:
			print('I dont know how to do that at the fish_market')

		#tailor
		if ccfg['butcher'] == 'gaul_soup':
			self.craft_gaul_soup()
		elif ccfg['butcher'] == 0:
			print('Skipping butcher crafting')
		else:
			print('I dont know how to do that at the butcher')



	def restock(self):
		rcfg = config['restock']
		if rcfg['fish_market']:
			self.restock_fish_market()
		else:
			print('Not restocking fish_market')

		if rcfg['butcher']:
			self.restock_butcher()
		else:
			print('Not restocking butcher')




if __name__ == '__main__':
	crafter = Craft()
	crafter.craft()
	crafter.restock()
	#crafter.town_grab()

