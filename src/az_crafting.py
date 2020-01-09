import os
import time
import json
import datetime
import numpy as np
import cv2
from az_code import *
from az_farmer import *
from az_imaging import ImageLoader
from az_cord_helper import CordHelper
from az_inv import Stock, Inventory
import pyscreenshot as ImageGrab
from PIL import ImageOps
from numpy import *
from pynput.mouse import Controller

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
craft_pos = (990, 716)
blank_spot = (517, 432) #(341, 373)
close_pos = (1074, 355)

# Crafting Positions
first_pos = (629, 424) # (564, 415)
second_pos = (629, 480) # (533, 477)
third_pos = (629, 550) # (513, 544)
fourth_pos = (629, 620) # (518, 610)
fifth_pos = (629, 690) # (513, 678)

# Stone Mason
stone_mason_pos = (751, 454)
stone_mason_build = (821, 454)

# Carpenter
carpenter_pos = (928, 465)
carpenter_build = (1000, 470)

# Blacksmith
blacksmith_pos = (1032, 510)
blacksmith_build = (1100, 513)

# Tailor
tailor_pos = (616, 642)
tailor_build = (684, 645) # TBD

#Leatherworker
leatherworker_pos = (721, 593)
leatherworker_build = (794, 595)

#Merchandise info
merch_pos_1 = (836, 468)
merch_pos_2 = (964, 460)
merch_pos_3 = (828, 600)
close_merch_pos = (1058, 401)
close_merch_pos_2 = (913, 627)

#Fish Market
fish_market_pos = (856, 632)
fish_market_build = (864, 698)
fish_market_restock = (913, 627)
fish_market_img = '/opt/dev/az/templates/fish_soup_vm_fb.png'
fish_soup_img = '/opt/dev/az/templates/inventory/items/fish_soup_single_2.png'

#Butcher
butcher_pos = (941, 678)
butcher_build = (964, 758)
butcher_restock = (1014, 688)
butcher_img = '/opt/dev/az/templates/gaul_soup_vm_fb.png'
gaul_soup_img = '/opt/dev/az/templates/inventory/items/gaul_soup_single_2.png'

#Tavern
tavern_pos = (792, 703)

#Water
water_well_pos = (823, 535)

#Foodpath
food_level_path = '../templates/food_level/'

#Potion
potion_pos = (235, 494)
brew_pos = (307, 492)
potion_pg_up = (509, 527)
potion_pg_dn = (510, 748)
potion_close = (1109, 353)
potion_list = ["major_potion_of_blocking", "major_potion_of_strength", "incredible_potion_of_knockout", "major_stonebreaker_potion"]
potion_dir = '../templates/potions/'


class Craft():
	def __init__(self):
		from az_farmer import town_grab, refresh_checker
		self.town_x = 442
		self.town_y = 300
		self.town_w = 800
		self.town_h = 450
		self.sell_cord_list = [(645, 460), (764, 460), (913, 460), (645, 600), (764, 600), (913, 600)]
		print("Crafting Module Engaged!")
		self.potion_crafting = (450, 350, 660, 420)
		self.potion_safe_spot = (746, 354)
		self.brew_path = '../templates/potions/brew/'
		refresh_checker()
		#is_popup()
		nav_to_town()


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


	def load_image_from_dir(self, item_dir):
		il = ImageLoader()
		img_obj_list = il.load_images_from_dir(item_dir)
		return img_obj_list


	def get_color_image(self, x=1, y=1, w=1250, h=920, tag='merch_col'):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, x+w, y+h)
		im = ImageGrab.grab(box)
		fn = "tmp_{}.png".format(tag)
		im.save(fn,'PNG')
		logger.info("Saved image: {}".format(fn))


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


	def craft_flagstone(self):
		""" Craft stone """
		if self.building_state(stone_mason_pos) == 1:
			move_and_click(stone_mason_pos, 1)
			move_and_click(blank_spot, 1)
			move_and_click(stone_mason_pos, 1)
			move_and_click(stone_mason_build, 1)
			move_and_click(third_pos, 1)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(craft_pos, 0.2)
			move_and_click(close_pos, 0.2)
			print("Crafting Flagstone")
		else:
			print("Stone Mason is busy, not crafting")


	def craft_milestone(self):
		""" Craft stone """
		buy_dye = (1018, 598)
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
			move_and_click(third_pos, 1)
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
			move_and_click(close_pos, 0.2)
			print("Crafting Flax")
		else:
			print("Tailor is busy, not crafting")


	def get_potion_images(self):
		print("Crafting Potions")
		nav_top_l(2)
		move_and_click(potion_pos, 1)
		move_and_click(brew_pos, 1)
		x, y, w, h = self.potion_crafting
		n = 5
		while n > 0:
			r = "potion_craft_{}".format(n)
			self.get_color_image(x, y, w, h, r)
			move_and_click(potion_pg_dn, 1)
			n -= 1


	def craft_potion(self, potion):
		print("Crafting Potions")
		nav_top_l(2)
		move_and_click(potion_pos, 1)
		move_and_click(brew_pos, 1)
		move_and_click(self.potion_safe_spot, 1)
		cord = self.potion_find(potion)
		move_and_click(cord, 1)
		move_and_click(self.potion_safe_spot, 1)
		print("Check if available")
		time.sleep(2)
		cord = self.potion_brew()
		if cord != False:
			move_and_click(cord, 1)
			move_and_click(cord, 1)
			move_and_click(cord, 1)
		move_and_click(potion_close, 1)

	def potion_find(self, potion):
		x, y, w, h = self.potion_crafting
		fp = '{}{}/'.format(potion_dir,potion)
		pages = 0
		while pages < 5:
			imgs = self.load_image_from_dir(fp)
			self.get_color_image(x, y, w, h, 'potion_craft')
			screen = cv2.imread('tmp_potion_craft.png')
			for img in imgs:
				result = cv2.matchTemplate(screen, img, method) # Does it match?
				fres = np.where(result >= 0.95)
				if fres[0].size == 0:
					pass
				elif fres[0].size > 1:
					cord = (int(fres[1][0]+x), int(fres[0][0]+y))
					#print("Potion: {} found @ {}".format(potion, cord))
					return cord
				else:
					cord = (int(fres[1]+x), int(fres[0]+y))
					#print("Potion: {} found @ {}".format(potion, cord))
					return cord
			pages += 1
			move_and_click(potion_pg_dn, 1)
		print("Didn't find {}".format(potion))
		return False


	def potion_brew(self):
		x, y, w, h = self.potion_crafting
		imgs = self.load_image_from_dir(self.brew_path)
		self.get_color_image(x, y, w, h, 'potion_craft')
		screen = cv2.imread('tmp_potion_craft.png')
		for img in imgs:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.95)
			if fres[0].size == 0:
				pass
			elif fres[0].size > 1:
				cord = (int(fres[1][0]+x), int(fres[0][0]+y))
				return cord
			else:
				cord = (int(fres[1]+x), int(fres[0]+y))
				return cord		
		return False

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
		x1 = 700
		x2 = 840
		y = 550
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
			#print("Found {} @ {} in slot {}".format(item_name, cord, click_cord))
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
			move_and_click(fish_market_pos, 1)


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
			move_and_click(butcher_pos, 1)


	def collect_tavern(self):
		move_and_click(tavern_pos, 1)
		#otherr


	def max_food_check(self):
		x, y, w, h = (1092, 158, 200, 80)
		self.get_color_image(x, y, w, h, 'fc')
		fll = self.load_image_from_dir(food_level_path)
		screen = cv2.imread('tmp_fc.png')
		for f in fll:
			try:
				result = cv2.matchTemplate(screen, f, method) # Does it match?
				fres = np.where(result >= 0.90)
				if fres[0].size == 0:
					pass
				elif fres[0].size > 1:
					print("Food Level full, do stuff breh!")
					return True
				else:
					print("Food Level full, do stuff breh!")
					return True		
			except:
				print("Somethings wrong in max_food_check")
		print("Food not full, keep grinding...")
		return False


	def get_water(self, n):
		if self.max_food_check() != False:	
			print("Fetching water {} times.".format(n))
			while n > 0:
				move_and_click(water_well_pos, 1)
				n -= 1
			print("Finished fetching water.")
		else:
			return False


	def water_level(self):
		max_water = 50
		s = Stock()
		water_count = s.count_item('water', '../templates/inventory/items/water/', 10)
		if water_count < max_water:
			water_counter = max_water-water_count
			if water_counter > 20: # Never collect more than 20 water in 1 shot.
				water_counter = 20
			print("Max water is {} and current water is {}".format(max_water, water_counter))
			self.get_water(water_counter)
		else:
			print("Water levels full, carry on your business")
			pass


	def craft(self):
		ccfg = config['crafting']
		print(ccfg)

		#stone mason
		if ccfg['stone_mason'] == 'stone':
			self.craft_stone()
		elif ccfg['stone_mason'] == 'milestone':
			self.craft_milestone()
		elif ccfg['stone_mason'] == 'flagstone':
			self.craft_flagstone()
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
		self.craft_stone() # Stone Mason
		self.craft_wood_plank() # Carpenter
		self.craft_nails() # Blacksmith
		self.craft_leather() # Leatherworker
		self.craft_gaul_soup() # Butcher
		self.craft_fish_soup() # Fish Market


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

		self.collect_tavern()



if __name__ == '__main__':
	#refresh_checker()
	nav_to_town()
	crafter = Craft()
	#crafter.craft_potion("incredible_potion_of_knockout")
	crafter.water_level()
	crafter.craft()
	crafter.restock()
	#nav_to_town()

