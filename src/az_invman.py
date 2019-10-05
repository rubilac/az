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
from pynput.mouse import Button, Controller
import numpy as np
import cv2
import shutil
import logging

# Globals #
json_files = ['items_mark.json', 'items_arty.json', 'items_pew.json']
pwd = os.path.realpath('..')
fixture_path = os.path.join(pwd, 'fixtures/')
item_file = '/opt/dev/az/fixtures/items.json'
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
mouse = Controller()


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


class HtmlGen():
	""" Generate an html file with a table of all the items """
	def __init__(self, json_files=[]):
		self.outfile = "inventory.html"
		self.header_info = 	"""	
						<html>
						<body>
						<p><font face='Verdana'>Inventory Overview</font></p>
						"""
		self.footer_info = """</body></html>"""
		self.full_inventory = []
		self.out_list = []
		if len(json_files)>0:	
			for i in json_files:
				data = load_file(i)
				data['uid'] = i
				self.full_inventory.append(data)
			logger.info("{} Files pre-loaded".format(len(json_files)))
			self.master_list = self.gen_master_item_list()
			self.master_data = self.pop_data()
			self.html = self.create_table()
			self.output_file(self.html)


	def load_json(self, json_file):
		data = load_file(json_file)
		logger.debug("{} file loaded".format(json_file))
		return data


	def load_json_set(self, json_files):
		self.full_inventory = []
		for i in json_files:
			data = load_file(i)
			self.full_inventory.append(data)
		logger.info("{} Files loaded".format(len(json_files)))
		return self.full_inventory


	def sortOther(self, val):
		""" TODO """ 
		return val['total']


	def create_table(self):
		"""
		Master Data
		[{
			"item_name": "amp",
			"count": [0,2,3]
			"total": 5
		}]
		"""
		col_names = self.get_col_names()
		rows = ""
		data = self.master_data
		data.sort(key = self.sortOther, reverse=True)
		for item in data:
			logger.info(item['item_name'], item['count'], item['total'])
			row = self.create_row(item['item_name'], item['count'])
			rows += row
		tbl = """<table border="1" style="border: 2px solid black; border-collapse: collapse">
				<tr height=30>
				<th><font face='Verdana'>Item Name</font></th>
				<th><font face='Verdana'>{}</font></th>
				<th><font face='Verdana'>{}</font></th>
				<th><font face='Verdana'>{}</font></th>
				<th><font face='Verdana'>Total</font></th>
				</tr>""".format(col_names[0], col_names[1], col_names[2])			
		close_tbl = "</table>"
		out = tbl+rows+close_tbl
		logger.info(out)
		return out


	def get_col_names(self):
		out_list = []
		col_list = list(x['uid'] for x in self.full_inventory)
		for col_name in col_list:
			out = col_name.split('.')
			out = out[0]
			out_list.append(out)
		return out_list


	def create_row(self, item_name, count):
		total = sum(count)
		row = """<tr height=30>
				<td width=300><font face='Verdana'>{}</font></td>
				<td style='background-color:grey; text-align:center' width=150><font face='Verdana'>{}</font></td>
				<td style='text-align:center' width=150><font face='Verdana'>{}</font></td>
				<td style='background-color:grey; text-align:center' width=150><font face='Verdana'>{}</font></td>
				<td style='text-align:center' width=150><font face='Verdana'>{}</font></td>
				</tr>""".format(item_name, count[0], count[1], count[2], total)
		return row


	def gen_master_item_list(self):
		master_item_list = []
		data = self.full_inventory
		for user in data:
			for item in user['il']:
				if item['item_name'] in master_item_list:
					continue
				else:
					master_item_list.append(item['item_name'])
		sorted_list = sorted(master_item_list)
		return sorted_list


	def pop_data(self):
		"""
		{
			"item_name": "amp",
			"count": [0,2,3]
			"total": 5
		}
		"""
		out_list = []
		for i in self.master_list:
			ci = {}
			ci['item_name'] = i
			ci['count'] = []
			for u in range(len(self.full_inventory)):
				for x in self.full_inventory[u]['il']:
					if x['item_name'] == i:
						stack = x['item_stacksize']
						cur = x['item_count_cur']
						if cur > 0:
							real_count = ((cur-1)*stack)+1
							ci['count'].append(real_count)
						else:
							ci['count'].append(0)
			ci['total'] = sum(ci['count'])
			out_list.append(ci)
		return out_list


	def data_gen(self):
		logger.info(self.full_inventory)
		return self.full_inventory


	def output_file(self, data):
		f = open(self.outfile, "w")
		f.write(str(data))
		logger.info("Inventory data written to {}".format(self.outfile))


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
		# Inventory is open @ (533, 414)
		self.method = cv2.TM_CCOEFF_NORMED
		self.threshold = 0.99
		self.screen_w = 2400
		self.screen_h = 2400
		self.end_of_bag = [32705332, 21902624, 32825199]
		self.del_list = [	
							32118004, 32706955, 30655535, 34591822
						]
		#self.items = load_file(item_file)
		self.inv_def = {
			"item_name" : "replace_me",
			"item_int" : 0,
			"item_max" : 100,
			"item_count_cur" : 0,
			"item_count_prev" : 0,
			"item_delete" :	False,
			"item_stacksize" : 5
			}


	def open_bag(self, seg='', threshold=0.88):
		"""
			Take a screen grab and locate the inventory icon. If it is found: click it
			If not quit
		"""
		template = read_image(inv_icon_img, cv2.IMREAD_GRAYSCALE)
		if seg == '':
			segment = ImageOps.grayscale(ImageGrab.grab(bbox=(1, 1, self.screen_w, self.screen_h)))
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
			return cord
		except TypeError:
			logger.critical("Cannot find inventory button, quitting...")
			raise Exception("Cannot find inventory button, quitting...")


	def reset_counter(self, file_name=item_file):
		""" 
			Copy the current counter to previous, and reset the current counter
		"""
		try:
			items = load_file(file_name)
			for item in items['il']:
				item['item_count_prev'] = item['item_count_cur']
				item['item_count_cur'] = 0
			with open(file_name, 'w') as outfile:
			    json.dump(items, outfile, indent=4, sort_keys=True)
			self.items = load_file(file_name)
			return True
		except:
			raise Exception("Counter reset failed.")


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
			logger.critical("Caught Exception as {}".format(e))
			raise Exception("Caught Exception as {}".format(e))
		
		logger.debug("Fres {}, Threshold {}".format(fres, threshold))
		
		try:
			cord = (int(fres[1]/2), int(fres[0]/2))
			logger.info("Inventory is open @ {}".format(cord))
			return cord
		except TypeError:
			logger.warning("Inventory is not open, open bag and continue")
			return False


	def get_image(self, x, y, width, length, tag="default", save=False):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageOps.grayscale(ImageGrab.grab(box))
		ts = int(time.time())
		if save:
			fn = "grayimg{}-{}.png".format(tag, ts)
			im.save(fn,'PNG')
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


	def add_item_to_store(self, item_int, item_file=item_file):
		""" 
			Given an item_int add the new inventory object to ../fixtures/items.json
		"""
		try:
			self.items = load_file(item_file)
			new_inv = self.inv_def
			new_inv['item_int'] = item_int
			self.items['il'].append(new_inv)
			with open(item_file, 'w') as outfile:
			    json.dump(self.items, outfile, indent=4, sort_keys=True)
			logger.info("Added new item to store with item_int: {}".format(item_int))
			self.items = load_file(item_file)
		except:
			raise Exception("Unable add item {} to store".format(item_int))


	def update_item_count(self, item_int, item_file=item_file):
		""" 
			Given an item_int update ../fixtures/items.json with the new count and write the update back to the file
		"""
		self.items = load_file(item_file)
		count = 0
		for item in self.items["il"]:
			if item["item_int"] == int(item_int):
				self.items['il'][count]["item_count_cur"] += 1
				item_name = self.items['il'][count]['item_name']
				with open(item_file, 'w') as outfile:
				    json.dump(self.items, outfile, indent=4, sort_keys=True)
				self.items = load_file(item_file)
				logger.debug("Updated: {} by 1".format(item_name))
				break
			count += 1


	def img_in_store(self, item_int, item_file=item_file):
		""" 
			Iterate through items in ../fixtures/items.json and update the current count if it exists 
			If the item does not exist in the store, add it to the store and try again.
		"""
		items = load_file(item_file)
		try:
			item_detail = list(filter(lambda x: x['item_int'] == item_int, items['il']))
			self.update_item_count(item_int)
			return dict(item_detail[0])
		except IndexError:
			logger.warning("Item_int not found, adding item to store with default values, please populate data")
			self.add_item_to_store(item_int)
			self.img_in_store(item_int)


	def get_inv_slots(self, bag_cord):
		""" Given the bags coordinates fetch the inventory slots and check if they exist in the store """
		inv_slots = self.inv_slot_gen(bag_cord)
		counter = 0
		for i_s in inv_slots:
			counter += 1
			img = self.get_color_image(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2, counter)
			if img == 32705332 or img == 21902624:
				logger.info("End of inventory, exitting!")
				sys.exit()
			else: 
				self.img_in_store(img)


	def inv_slot_gen(self, inv_cord):
		""" Given the inventory coordinate, return the coords for each inventory slot """
		x = inv_cord[0]-145
		y = inv_cord[1]+102
		inv_bx = 100
		inv_by = 100
		iyd = 179
		ixd = 165
		inv_1 = (x, y, x+inv_bx, y+inv_by)
		inv_2 = (x+ixd, y, x+ixd+inv_bx, y+inv_by)
		inv_3 = (x+ixd+ixd, y, x+ixd+ixd+inv_bx, y+inv_by)
		inv_4 = (x, y+iyd, x+inv_bx, y+iyd+inv_by)
		inv_5 = (x+ixd, y+iyd, x+ixd+inv_bx, y+iyd+inv_by)
		inv_6 = (x+ixd+ixd, y+iyd, x+ixd+ixd+inv_bx, y+iyd+inv_by)
		inv_slots = [inv_1, inv_2, inv_3, inv_4, inv_5, inv_6]
		return inv_slots


	def inv_slot_sell_gen(self, slot_cord, slot):
		""" Given the slot coordinate, return the coords for each slots sell button """
		sx = slot_cord[0]+75
		sy = slot_cord[1]+110
		cord = (sx, sy)
		return cord


	def inv_nav_left(self, bag_cord):
		""" Function to navigate the inventory widget right based on anchor """
		left_cord = (bag_cord[0]-200, bag_cord[1]+250)
		move_and_click(left_cord)
		logger.info("Navigating inventory left")


	def inv_nav_right(self, bag_cord):
		""" Function to navigate the inventory widget right based on anchor """
		right_cord = (bag_cord[0]+350, bag_cord[1]+250)
		move_and_click(right_cord)
		logger.info("Navigating inventory right")


	def refresh_inventory(self):
		""" 
			Iterates through a players inventory and stores the current value in a json file.
			Resets the counter and stores 1 previous set
			Opens the bag if not already open
		"""
		logger.info("Refreshing Inventory")
		move_and_click((450, 240))
		try:
			cord = self.open_bag_check()
		except:
			self.open_bag()
		self.reset_counter(item_file)
		bag_number = 1
		while True:
			logger.info("Refreshing bag number: {}".format(bag_number))
			self.get_inv_slots(cord)
			self.inv_nav_right(cord)
			bag_number += 1


	def delete_item(self, bag_cord, item_int, slot):
		"""
			Given an item_int, find the item_int inv_slot on the page and execute the delete sequence
		"""
		mbx = bag_cord[0]
		mby = bag_cord[1]+300
		minus = (mbx, mby)
		confirm_sell = (bag_cord[0]+80, bag_cord[1]+370)
		all_slots = self.inv_slot_gen(bag_cord)
		tar_slot = all_slots[slot]
		x, y, bx, by = tar_slot
		sell_button = self.inv_slot_sell_gen((x, y), slot)
		logger.debug("{} tar_slot: {}, sell_button: {}".format(qt(), tar_slot, sell_button))
		mousePos(sell_button)
		move_and_click(sell_button)
		time.sleep(1)
		mousePos(minus)
		move_and_click(minus)
		time.sleep(1)
		mousePos(confirm_sell)
		move_and_click(confirm_sell)
		time.sleep(1)
		move_and_click((450, 240))


	def delete(self, inv_slots, bag_cord):
		"""
			Given a list of inv_slots and the bag coordinates:
			exit if we hit the end of the inventory
			if the item is in the delete list, execute the delete_item and start the cleaner again
		"""
		counter = 0
		for i_s in inv_slots:
			logger.debug("del_list: {}".format(self.del_list))
			img = self.get_color_image(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2, counter)
			logger.debug("Getting color image of dimenstions: x: {}, y: {}, w: {}, h: {}".format(i_s[0]*2, i_s[1]*2, i_s[2]*2, i_s[3]*2))
			if img in self.end_of_bag:
				logger.info("End of inventory, exitting!")
				break
				#sys.exit()
			elif img in self.del_list: 
				logger.debug("img: {}".format(img))
				self.delete_item(bag_cord, img, counter)
				idx = self.del_list.index(img)
				logger.info("Found item to delete, deleting {}".format(self.del_list[idx]))
				return self.bag_cleaner(del_list, bag_cord, True)
			else:
				logger.info("Nothing to delete here!")
			counter += 1


	def bag_cleaner(self, del_list, bag_cord=0, bypass=True):
		""" 
			Function to get the current bag page and initiate a delete if the item is found in the 
			delete list.
			It will skip the bag check if the bypass is used as a workflow optimization.
		"""	
		if bypass == False:
			logger.info("Starting delete without bypass")
			try:
				bag_cord = self.open_bag_check()
				inv_slots = self.inv_slot_gen(bag_cord)
				logger.debug("Bag_cord {}, Inv_slots: {} ".format(bag_cord, inv_slots))
				self.delete(inv_slots, bag_cord)
				logger.info("Completed bag delete")
			except TypeError:
				logger.info("Bag is not open, opening bag and trying bag delete again")
				self.open_bag() # fix the problem and restart the function
				bag_cord = self.open_bag_check()
				return self.bag_cleaner(del_list, bag_cord, True)
		else:
			logger.info("Starting delete with bypass")
			inv_slots = self.inv_slot_gen(bag_cord)
			self.delete(inv_slots, bag_cord)


	def cleanup_loop(self, bag_cord):
		""" 
			Function to loop through bags and execute a cleanup until we reach the end of the items in the bag
		"""
		bag_number = 1
		logger.info("Starting bag cleanup")
		logger.info("Bag cords @ : {}".format(bag_cord))
		while True:
			print("Cleaning Bag Number: {}".format(bag_number))
			self.bag_cleaner(bag_cord)
			logger.info("Cleaning bag number: {}".format(bag_number))
			self.inv_nav_right(bag_cord)
			logger.debug("Navigating right in inventory")
			bag_number += 1


	def save_inventory_to_file(self, new_file):
		""" This function consumes the master ../fixtures/items.json file and creates a player specific copy """
		try:
			shutil.copyfile(item_file, new_file)
			logger.info("../fixtures/items.json was copied to {}".format(new_file))
		except:
			print("Saving ../fixtures/items.json failed")
			logger.critical("Could not copy ../fixtures/items.json to {}".format(new_file))


	def cleanup_inventory(self):
		""" 
			Function to coordinate the cleanup of the active inventory according to a whitelist of deletable iterms
			This function will open the bag if it cannot see that bag is open
		"""
		move_and_click((450, 240)) # Focus brower frame. TODO: make this anchor aware
		try:
			bag_cord = self.open_bag_check() # Checks for bag and opens if its not open 	
			self.cleanup_loop(bag_cord)
		except:
			logger.error("Bag is not open, opening bag and trying cleanup inventory again")
			self.open_bag()
			return self.cleanup_inventory()


if __name__ == '__main__':
	inventory = Inventory()
	inventory.cleanup_inventory()
	