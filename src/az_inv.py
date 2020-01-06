import os
import sys
import time
import json
import datetime
from az_code import *
from az_farmer import *
from az_imaging import *
import pyscreenshot as ImageGrab
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

boar_skin_img_loc = config['inventory']['boar_skins']
entrails_img_loc = config['inventory']['entrails']
fish_img_loc = config['inventory']['fish']
iron_scraps_img_loc = config['inventory']['iron_scraps']


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
		self.screen_x = 70
		self.screen_y = 160
		self.screen_w = 1488
		self.screen_h = 925
		self.search_pos = (466, 395)
		self.search_clear = (542, 394)
		#self.anchor = get_anchor()
		self.img_path = '/opt/dev/az/templates/inventory/items/'
		self.sell_cord_list = [(687, 519), (815, 518), (939, 518), (679, 663), (813, 663), (943, 664)]
		self.sell_cord_sell = (781, 639)
		self.sell_cord_minus = (712, 592)


	def open_bag(self):
		cord = (1433, 822)
		move_and_click(cord, 1)


	def open_bag_check(self, seg='', threshold=0.99):
		"""
			Grab a 2200 x 2200 piece of the screen and return the cord of the inventory.png template
			if the inventory is open, otherwise return False
		"""
		template = read_image(inv_img, cv2.IMREAD_GRAYSCALE)
		if seg == '':
			segment = ImageOps.grayscale(ImageGrab.grab(bbox=(self.screen_x, self.screen_y, self.screen_w, self.screen_h)))
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
			cord = (int(fres[1]), int(fres[0]))
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


	def get_image(self, x=70, y=160, width=1488, length=925, tag="default", save=True):
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


	def get_color_image(self,  x=70, y=160, width=1488, length=925, tag="default", save=True):
		"""
			Given x, y cords and width and length size, take a color image and return the summed value
			of all 3 rgb ints.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageGrab.grab(box)
		if save:
			fn = "colorimg-{}.png".format(tag)
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
		move_and_click(self.search_pos, 0.5)
		key.type(item_name)
		key.press(Key.enter)
		key.release(Key.enter)
		time.sleep(6)


	def search_clear_bar(self):
		""" Clear Search bar """
		move_and_click(self.search_clear, 1)
		move_and_click(self.search_clear, 1)


	def inv_nav_left(self, bag_cord):
		""" 
			Function to navigate the inventory widget right based on anchor
		"""
		left_cord = (566, 551)
		move_and_click(left_cord)
		logger.info("Navigating inventory left")


	def inv_nav_right(self):
		""" 
			Function to navigate the inventory widget right based on anchor 
		"""
		right_cord = (986, 551)
		move_and_click(right_cord)
		logger.info("Navigating inventory right")


	def item_in_inventory(self, item_path, item_name):
		"""
			Given an item name and stacks to keep (int)
			TODO: What if I dont have any?
		"""
		slot_list = []
		self.search_item(item_name) # Filter to item in inventory
		item = cv2.imread(item_path)
		self.get_color_image() # Load item template
		screen = cv2.imread('colorimg-default.png')
		try:
			result = cv2.matchTemplate(screen, item, self.method) # Load current screen
			fres = np.where(result >= 0.95)
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


	def delete_items_from_pane(self, item_path, item_name):
		first_cord = self.get_first_pos(item_path, item_name)
		print("+++++++++Deleting {} - {} time(s)".format(item_name, first_cord[1]))
		self.delete_item(first_cord[0][1], first_cord[1])


	def delete_all_of_item(self, item_path, item_name):
		item_exists = self.item_in_inventory(item_path, item_name)
		while item_exists != 1:
			self.delete_items_from_pane(item_path, item_name)
			refresh_checker()
			time.sleep(5)
			self.open_bag()
			item_exists = self.item_in_inventory(item_path, item_name)


	def get_first_pos(self, item_path, item_name):
		tmp = self.item_in_inventory(item_path, item_name)
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
			self.close()
		

	def delete_item(self, cord, num_sells):
		#print("Deleting Item {} times".format(num_sells))
		while num_sells > 0:
			move_and_click(cord, 0.5)
			move_and_click(self.sell_cord_minus, 0.5)
			move_and_click(self.sell_cord_sell, 0.5)
			num_sells -= 1


	def get_sell_button(self, cord):
		""" 5
			cord = (1000, 2000) 
			pos1 = ( x < 750,  y < 550)
			pos2 = (<1200, >800<1200)
			pos3 = (<1200, >1200)
			pos4 = (>1200, <800)
			pos5 = (>1200, >800<1200)
			pos6 = (>1200, >1200)

		"""
		cord = (cord[0]+self.screen_y, cord[1]+self.screen_x)
		x1= 700
		x2= 840
		y= 530
		print("Item found @ {}".format(cord))
		sell_buttons = self.sell_cord_list
		if cord[0] < y and cord[1] < x1:
			out = [1, self.sell_cord_list[0]]
			return out
		if cord[0] < y and x1 < cord[1] < x2:
			out = [2, self.sell_cord_list[1]]
			return out
		if cord[0] < y and cord[1] > x2:
			out = [3, self.sell_cord_list[2]]
			return out
		if cord[0] > y and cord[1] < x1:
			out = [4, self.sell_cord_list[3]]
			return out
		if cord[0] > y and x1 < cord[1] < x2:
			out = [5, self.sell_cord_list[4]]
			return out
		if cord[0] > y and cord[1] > x2:
			out = [6, self.sell_cord_list[5]]
			return out


	def close(self):
		move_and_click((992, 374), 1)


class Stock():
	def __init__(self):
		self.il = ImageLoader()
		self.inv = Inventory()
		self.inv.open_bag_force()
		self.method = cv2.TM_CCOEFF_NORMED
		self.threshold = 0.98
		self.x = 430
		self.y = 340
		self.w = 1000
		self.h = 730
		self.slot_1 = ()
		self.slot_2 = ()
		self.slot_3 = ()
		self.slot_4 = ()
		self.slot_5 = ()
		self.slot_6 = ()


	def count_page(self, item_name, dir_path):
		self.inv.get_color_image(self.x, self.y, self.w, self.h, 'stock')
		template_list = self.il.load_images_from_dir(dir_path)
		screen = cv2.imread('colorimg-stock.png')
		unflattened = []
		for template in template_list:
			result = cv2.matchTemplate(screen, template, self.method)
			fres = np.where(result >= self.threshold)
			slot_cords = list(zip(fres[1]+self.x, fres[0]+self.y))
			out = []
			for entry in slot_cords:
				out.append(self.get_inv_slot(entry))
			unflattened.append(out)
		flattened = []
		for i in unflattened:
			flattened = flattened + i
		out = sorted(np.unique(flattened))
		return out


	def count_item(self, item_name, dir_path, stack_size):
		self.inv.search_item(item_name)
		first = self.count_page(item_name, dir_path)
		count = len(first)
		while 6 in first:
			self.inv.inv_nav_right()
			first = self.count_page(item_name, dir_path)
			count += len(self.count_page(item_name, dir_path))
		count = (count - 1)*stack_size
		print("{}-{} {}".format(count, count+stack_size, item_name))
		self.inv.close()
		return count


	def get_item(self, item_name):
		self.inv.search_item(item_name)
		self.inv.get_color_image(self.x, self.y, self.w, self.h, 'get_stock')


	def get_inv_slot(self, cord):
		""" 5
			cord = (1000, 2000) 
			pos1 = ( x < 750,  y < 550)
			pos2 = (<1200, >800<1200)
			pos3 = (<1200, >1200)
			pos4 = (>1200, <800)
			pos5 = (>1200, >800<1200)
			pos6 = (>1200, >1200)

		"""
		x1= 710
		x2= 840
		y= 530
		if cord[1] < y and cord[0] < x1:
			out = 1
			return out
		elif cord[1] < y and x1 < cord[0] < x2:
			out = 2
			return out
		elif cord[1] < y and cord[0] > x2:
			out = 3
			return out
		elif cord[1] > y and cord[0] < x1:
			out = 4
			return out
		elif cord[1] > y and x1 < cord[0] < x2:
			out = 5
			return out
		elif cord[1] > y and cord[0] > x2:
			out = 6
			return out
		else:
			print("Couldn't find a slot... weird!")


def delete_inv():
	inventory = Inventory()
	#inventory.get_color_image()
	refresh_checker()
	inventory.delete_all_of_item(boar_skin_img_loc, 'boar skins')
	refresh_checker()
	inventory.delete_all_of_item(entrails_img_loc, 'entrails')
	refresh_checker()
	inventory.delete_all_of_item(fish_img_loc, 'fish')
	refresh_checker()
	inventory.delete_all_of_item(iron_scraps_img_loc, 'iron scraps')
	inventory.close()	


if __name__ == '__main__':
	delete_inv()
	#s = Stock()
	#s.count_item('stone blocks', '../templates/inventory/items/stone_blocks/', 10)



#TODO: Horns