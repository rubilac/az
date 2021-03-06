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


def read_image(image, img_type):
	img = cv2.imread(image, img_type)
	try:
		img.any() #Checks if the ps is not a none
		return img
	except:
		logger.critical("Invalid input file: {}".format(image))
		raise Exception("Invalid input file: {}".format(image))


def get_match_result(ps, template, method, threshold):
	result = cv2.matchTemplate(ps, template, method)
	fres = np.where(result >= threshold)
	if len(fres[0]) > 1:
		raise Exception("Too many values found in results, refine threshold")
	elif len(fres[0]) == 0:
		raise Exception("No values found in results please refine threshold")
	else:
		return fres


class Inventory():
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
		self.method = cv2.TM_CCOEFF_NORMED
		self.threshold = 0.90
		self.screen_x = 1
		self.screen_y = 1
		self.screen_w = 2400
		self.screen_h = 2400
		self.end_of_bag = [32705332, 21902624]
		self.del_list_3 = ['boar bones', 'boar_skins', 'boar_tooth', 'crabs', 'egyptian fish', 'gold ore', 'iron ore', 'lobsters', 'mushrooms', 'oats', 'oysters', 'smelly fish', 'stone blocks']
		self.del_list_2 = []
		self.del_list_1	= []
		self.del_list_0	= ['fish', 'entrails', 'sand']
		self.search_pos = (-852, 265)
		self.search_clear = (-802, 265)
		self.search_result_pos = (-888, 340)
		self.anchor = get_anchor()
		self.img_path = '/opt/dev/az/templates/inventory/items/'
		self.sell_cord_list = [(-632, 423), (-456, 421), (-303, 424), (-633, 601), (-468, 600), (-302, 603)]
		self.sell_cord_sell = (-503, 574)
		self.sell_cord_minus = (-589, 512)


	def open_bag(self, seg='', threshold=0.88):
		"""
			Take a screen grab and locate the inventory icon. If it is found: click it
			If not quit
		"""
		template = read_image(inv_icon_img, cv2.IMREAD_GRAYSCALE)
		if seg == '':
			segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1, 1, self.screen_w, self.screen_h)))
			#self.get_image(1, 1, self.screen_w, self.screen_h,"default", True)
			ps = np.array(segment.getdata(), dtype='uint8').reshape((segment.size[0], segment.size[1],-1))
		else:
			try:
				ps = read_image(seg, cv2.IMREAD_GRAYSCALE)
			except:
				raise Exception("Could not read image: {}".format(seg))
		try:
			fres = get_match_result(ps, template, self.method, threshold)
		except Exception as e:
			logger.critical("Caught Exception as {}".format(e))
			raise Exception("Caught Exception as {}".format(e))

		logger.debug("Opening Bag Fres: {}".format(fres))
		try:
			cord = (int(fres[1]/2+5), int(fres[0]/2+5))
			logger.info("Found Inventory Button @ {}, openning inventory".format(cord))
			move_and_click(cord)
			move_and_click(cord)
			return cord
		except TypeError:
			logger.critical("Cannot find inventory button, quitting...")
			raise Exception("Cannot find inventory button, quitting...")


	def open_bag_check(self, seg='', threshold=0.99):
		"""
			Grab a 2200 x 2200 piece of the screen and return the cord of the inventory.png template
			if the inventory is open, otherwise return False
		"""
		template = read_image(inv_img, cv2.IMREAD_GRAYSCALE)
		if seg == '':
			segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1,1,self.screen_w,self.screen_h)))
			ps = np.array(segment.getdata(), dtype='uint8').reshape((segment.size[0], segment.size[1],-1))
		else:
			try:
				ps = read_image(seg, cv2.IMREAD_GRAYSCALE)
			except:
				raise Exception('Unable to load open_bag_check images.')
		
		try:
			fres = get_match_result(ps, template, self.method, threshold)
		except Exception as e:
			logger.critical("Bag not open: {}".format(e))
			return False
		
		logger.debug("Fres {}, Threshold {}".format(fres, threshold))
		
		try:
			cord = (int(fres[1]/2), int(fres[0]/2))
			logger.info("Inventory is open @ {}".format(cord))
			return cord
		except TypeError:
			logger.warning("Inventory is not open, open bag and continue")
			return False


	def open_bag_force(self):
		""" Just open it man """

		cord = self.open_bag_check()
		if cord == False:
			self.open_bag()


	def get_image(self, x=1, y=1, width=2400, length=2400, tag="default", save=True):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageOps.grayscale(ImageGrab.grab(box))
		#ts = int(time.time())
		if save:
			fn = "gray-{}.png".format(tag)
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


	def load_image(self, item_name):
		img_full_path = '{}{}.png'.format(self.img_path, item_name) 
		img_tmp = cv2.imread(img_full_path)
		return img_tmp


	def search_item(self, item_name):
		""" given and item name, we will search for it """
		self.open_bag_force()
		self.search_clear_bar()
		secure_click(self.search_pos, self.anchor, 0.5)
		key.type(item_name)
		key.press(Key.enter)
		key.release(Key.enter)
		time.sleep(5)


	def search_clear_bar(self):
		""" Clear Search bar """
		secure_click(self.search_clear, self.anchor, 1)
		secure_click(self.search_clear, self.anchor, 1)


	def inv_nav_left(self, bag_cord):
		""" 
			Function to navigate the inventory widget right based on anchor
		"""
		left_cord = (bag_cord[0]-200, bag_cord[1]+250)
		move_and_click(left_cord)
		logger.info("Navigating inventory left")


	def inv_nav_right(self, bag_cord):
		""" 
			Function to navigate the inventory widget right based on anchor 
		"""
		right_cord = (bag_cord[0]+350, bag_cord[1]+250)
		move_and_click(right_cord)
		logger.info("Navigating inventory right")


	def item_in_inventory(self, item_name):
		"""
			Given an item name and stacks to keep (int)
			TODO: What if I dont have any?
		"""
		slot_list = []
		self.search_item(item_name) # Filter to item in inventory
		item = self.load_image(item_name)
		self.get_image() # Load item template
		screen = cv2.imread('gray-default.png')
		try:
			result = cv2.matchTemplate(screen, item, method) # Load current screen
			fres = np.where(result >= 0.99)
			slots = zip(fres[0], fres[1])
			slot_set = set(slots)
			count = 0
			for i in slot_set:
				count += 1
				slot_list.append(i)
			out = [slot_list, count]
			if out == [[], 0]:
				print("No item {} found".format(item_name))
				return 1
			else:
				return out
		except:
			print("Error, seems dodge")
			return 2 # if I dont find anythin, just return 1


	def delete_items_from_pane(self, item_name):
		first_cord = self.get_first_pos(item_name)
		print("First sell button @: {} Position {} - Delete {} time(s)".format(first_cord[0][1], first_cord[0][0], first_cord[1]))
		self.delete_item(first_cord[0][1], first_cord[1])


	def delete_all_of_item(self, item_name):
		item_exists = self.item_in_inventory(item_name)
		while item_exists != 1:
			self.delete_items_from_pane(item_name)
			item_exists = self.item_in_inventory(item_name)


	def get_first_pos(self, item_name):
		tmp = self.item_in_inventory(item_name)
		if tmp != 1:
			cord_list = tmp[0]
			num_items = tmp[1]
			sell_list = []
			for i in cord_list:
				sell_list.append(self.get_sell_button(i))
			sell_list.sort()
			first_cord = sell_list[0]
			return first_cord, num_items
		else:
			print("Nothing to see here, move along!")
		

	def delete_item(self, cord, num_sells):
		print("Deleting Item {} times".format(num_sells))
		while num_sells > 0:
			secure_click(cord, self.anchor, 1)
			secure_click(self.sell_cord_minus, self.anchor, 1)
			secure_click(self.sell_cord_sell, self.anchor, 1)
			num_sells -= 1


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


	def close(self):
		secure_click((-239, 244), self.anchor, 1)


	def delete_keep_n(self, cord, num_sells,  n):
		pass




if __name__ == '__main__':
	inventory = Inventory()
	is_popup()
	inventory.delete_all_of_item('boar skins')
	is_popup()
	inventory.delete_all_of_item('entrails')
	is_popup()
	inventory.delete_all_of_item('fish')
	inventory.close()
	#inventory.delete_items_from_pane('fish')
	#inventory.delete_items_from_pane('entrails')
	#inventory.delete_items_from_pane('boar skins')