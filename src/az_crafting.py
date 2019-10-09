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
blank_spot = (-974, 242)
close_pos = (-139, 216)



first_pos = (-587, 291)
second_pos = (-671, 393)
fourth_pos = (-686, 548)
stone_mason_pos = (-668, 321)
stone_mason_build = (-585, 307)
carpenter_pos = (-458, 320)
carpenter_build = (-364, 327)
blacksmith_pos = (-328, 383)
blacksmith_build = (-236, 391)
tailor_pos = (-837, 549)

#Merchandise info
merch_pos_1 = (-432, 383)
merch_pos_2 = (-263, 383)
merch_pos_3 = (-432, 558)
close_merch_pos = (-158, 271)
close_merch_pos_2 = (-242, 304)

#Fish Market
fish_market_pos = (-546, 535)
fish_market_build = (-533, 612)
fish_market_restock = (-470, 528)
fish_market_img = '/opt/dev/az/templates/fish_soup.png'
fish_soup_img = '/opt/dev/az/templates/inventory/items/fish_soup_single.png'

#Butcher
butcher_pos = (-432, 599)
butcher_build = (-404, 691)
butcher_restock = (-341, 607)
butcher_img = '/opt/dev/az/templates/gaul_soup.png'
gaul_soup_img = '/opt/dev/az/templates/inventory/items/gaul_soup_single.png'



#Leatherworker
leatherworker_pos = (-705, 488)
leatherworker_build = (-623, 487)



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
		self.sell_cord_list = [(-668, 382), (-509, 395), (-342, 383), (-664, 543), (-503, 550), (-344, 560)]
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


	def get_image(self, x=1, y=1, width=2400, length=2400, save=True):
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
		secure_mouse_over(building,self.anchor, 1) # mouseover building
		town_grab(self.town_x, self.town_y, self.town_w, self.town_h) # screengrab town
		self.ready_state = is_ready()
		return self.ready_state


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
			print("Carpenter is busy, not crafting")


	def craft_fish_soup(self):
		""" Craft Fish Soup """
		if self.building_state(fish_market_pos) == 1:
			secure_click(fish_market_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(fish_market_pos,self.anchor, 1)
			secure_click(fish_market_build,self.anchor, 1) 
			secure_click(second_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Fish Soup")
		else:
			print("Fish Market is busy, not crafting")


	def craft_iron_bar(self):
		""" Craft Bar """
		if self.building_state(blacksmith_pos) == 1:
			secure_click(blacksmith_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(blacksmith_pos,self.anchor, 1)
			secure_click(blacksmith_build,self.anchor, 1) 
			secure_click(first_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Iron Bar")
		else:
			print("Blacksmith is busy, not crafting")


	def craft_nails(self):
		""" Craft Bar """
		if self.building_state(blacksmith_pos) == 1:
			secure_click(blacksmith_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(blacksmith_pos,self.anchor, 1)
			secure_click(blacksmith_build,self.anchor, 1) 
			secure_click(fourth_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Nails")
		else:
			print("Blacksmith is busy, not crafting")


	def craft_gaul_soup(self):
		""" Craft Gaul Soup """
		if self.building_state(butcher_pos) == 1:
			secure_click(butcher_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(butcher_pos,self.anchor, 1)
			secure_click(butcher_build,self.anchor, 1) 
			secure_click(first_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Gaul Soup")
		else:
			print("Butcher is busy, not crafting")


	def craft_leather(self):
		""" Craft Gaul Soup """
		if self.building_state(leatherworker_pos) == 1:
			secure_click(leatherworker_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(leatherworker_pos,self.anchor, 1)
			secure_click(leatherworker_build,self.anchor, 1) 
			secure_click(first_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Leather")
		else:
			print("Leatherworker is busy, not crafting")


	def craft_grease(self):
		""" Craft Gaul Soup """
		if self.building_state(leatherworker_pos) == 1:
			secure_click(leatherworker_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(leatherworker_pos,self.anchor, 1)
			secure_click(leatherworker_build,self.anchor, 1) 
			secure_click(fourth_pos,self.anchor, 1)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(craft_pos,self.anchor, 0.2)
			secure_click(close_pos,self.anchor, 0.2)
			print("Crafting Grease")
		else:
			print("Leatherworker is busy, not crafting")


	def restock_state(self, building, img_path):
		# mouseover building
		# take snapper
		# if merch exists return false
		# otherwise return true
		secure_mouse_over(building,self.anchor, 3) # mouseover building
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
		secure_click(pos, self.anchor, 1) # Click Merch pos, this will open up inventory frame
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
			secure_click(click_cord, self.anchor, 1)
			print("Loading {} in slot {}".format(item_name, pos))
		except:
			print("No {} found! Make some!".format(item_name))
			return 1


	def load_stock_slots(self, stock, img_path):
		self.load_stock(stock, img_path, merch_pos_1)
		self.load_stock(stock, img_path, merch_pos_2)
		self.load_stock(stock, img_path, merch_pos_3)
		secure_click(close_merch_pos, self.anchor, 1)


	def restock_fish_market(self):
		if self.restock_state(fish_market_pos, fish_market_img) == 1:
			print("Restocking Fish Market")
			secure_click(fish_market_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(fish_market_pos,self.anchor, 1)
			secure_click(fish_market_restock,self.anchor, 1)
			self.load_stock_slots('fish_soup', fish_soup_img)
			secure_click(close_merch_pos, self.anchor, 1)
		else:
			print("Fish market full!")


	def restock_butcher(self):
		if self.restock_state(butcher_pos, butcher_img) == 1:
			print("Restocking Butcher!")
			secure_click(butcher_pos,self.anchor, 1)
			secure_click(blank_spot,self.anchor, 1)
			secure_click(butcher_pos,self.anchor, 1)
			secure_click(butcher_restock,self.anchor, 1)
			self.load_stock_slots('gaul_soup', gaul_soup_img)
			secure_click(close_merch_pos, self.anchor, 1)
		else:
			print("Butcher full!")


	def craft(self):
		self.craft_stone() # Stone Mason
		self.craft_wood_plank() # Carpenter
		self.craft_nails() # Blacksmith
		self.craft_grease() # Leatherworker
		self.craft_gaul_soup() # Butcher
		self.craft_fish_soup() # Fish Market


	def restock(self):
		self.restock_fish_market()
		self.restock_butcher()



if __name__ == '__main__':
	crafter = Craft()
	crafter.craft()
	crafter.restock()

