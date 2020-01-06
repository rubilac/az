#az_brawl

import os
import time
import json
from datetime import datetime
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
from az_imaging import ImageLoader

config = toml.load('.config')

method =  cv2.TM_CCOEFF_NORMED

def curr_time():
	now = datetime.datetime.now()
	current_time = now.strftime("%y%m%d%H%M%S")
	return current_time


class Brawl():
	def __init__(self):
		self.ring_pos = (916, 416)
		self.challenge = (937, 343)
		self.brawl_screen = (420, 340, 1150, 730)
		self.brawl_item_screen = (555, 417, 1000, 700)
		self.place_bet_pos = (777, 540)
		self.fight_pos = (787, 740)
		self.skip_pos = (775, 735)
		self.close_pos = (1123, 362)
		self.decline = (855, 715)
		self.decline_confirm = (860, 612)
		self.cancel_recovery = (938, 437)
		self.close_item_pos = (988, 430)
		self.remove_shield = (849, 630)
		self.item_left_arrow = (571, 552)
		self.item_right_arrow = (985, 551)
		self.item_first_slot = (647, 490)
		self.next_opp = (1085, 506)
		# Brawlers
		self.worker = [(562, 615), 'worker']
		self.edifis = [(645, 615), 'edifis']
		self.ekonomikrisis = [(746, 615), 'ekonomikrisis']
		self.pointandclix = [(811, 615), 'pointandclix']
		self.lunatix = [(903, 615), 'lunatix']
		self.democratix = [(994, 615), 'democratix']
		self.ironix = [(562, 680), 'ironix']
		self.baltix = [(658, 680), 'baltix']
		self.lyrix = [(738, 680), 'lyrix']
		self.brawler_list = ['worker', 'edifis', 'ekonomikrisis', 'pointandclix', 'lunatix', 'ironix', 'baltix', 'democratix', 'lyrix']
		self.brawler_path = '../templates/brawl/villagers/'
		self.full_brawler_list = [self.pointandclix, self.worker, self.lunatix, self.ekonomikrisis, self.ironix, self.lyrix, self.edifis, self.democratix, self.baltix]
		# Squads
		self.squad_1 = [self.pointandclix[0], self.worker[0], self.lunatix[0]]
		self.squad_2 = [self.ekonomikrisis[0], self.ironix[0], self.lyrix[0]]
		self.squad_3 = [self.edifis[0], self.democratix[0], self.baltix[0]]
		self.squad_list = [self.squad_1, self.squad_2, self.squad_3]
		self.squad_loser = [self.pointandclix[0], self.democratix[0], self.lunatix[0]]	
		self.item_list = ['coal', 'salt', 'rockoil']
		self.equipment_list = ['carpet', 'obelisk']
		self.item_dir = '../templates/brawl/'
		self.equipment_dir = '../templates/brawl/equipment/'
		# Potions
		self.first_pot_pos = (689, 510)
		self.item_pos = ()



	def open_ring(self):
		nav_to_town()
		move_and_click(self.ring_pos, 1)
		move_and_click(self.challenge, 1)


	def get_image(self, x=400, y=330, width=1150, length=760, tag="brawl"):
		"""
			Given x, y cords and width and length size, take a grayscale image and return the
			summed value.
			Option to save the image is off by default.
		"""
		box = (x, y, width, length)
		im = ImageGrab.grab(box)
		fn = "tmp_{}.png".format(tag)
		im.save(fn,'PNG')
		return


	def load_image_from_dir(self, item_dir):
		il = ImageLoader()
		img_obj_list = il.load_images_from_dir(item_dir)
		return img_obj_list


	def all_available(self):
		self.open_ring()
		time.sleep(5)
		self.get_image()
		img = cv2.imread('../templates/brawl/all_available.png')
		screen = cv2.imread('tmp_brawl.png')
		try:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.95)
			if fres[0].size == 0:
				print("Not all brawlers available! Setup manual squads")
			elif fres[0].size >= 1:
				print("All brawlers available, lets go")
				return True
		except:
			print("Not all brawlers available! try again later")
			move_and_click(self.close_pos, 1)


	def villager_available(self, villager):
		dir_path = '{}{}/'.format(self.brawler_path, villager)
		self.get_image()
		screen = cv2.imread('tmp_brawl.png')
		img_obj_list = self.load_image_from_dir(dir_path)
		for img_obj in img_obj_list:
			try:
				result = cv2.matchTemplate(screen, img_obj, method) # Does it match?
				fres = np.where(result >= 0.90)
				if fres[0].size == 0:
					#print("{} not available".format(villager))
					return 0
				elif fres[0].size >= 1:
					print("{} available".format(villager))
					return 1
			except:
				print("Couldnt figure out villager availability")
				return False


	def villager_gettr(self, villager_string):
		for i in self.full_brawler_list:
			if villager_string in i:
				return i[0]


	def whose_available(self):
		available = []
		for villager in self.brawler_list:
			if self.villager_available(villager) == 1:
				available.append(villager)
			else:
				pass
		print(available)
		return available


	def item_far_left(self):
		print()
		x = 7
		while x > 0:
			move_and_click(self.item_left_arrow)
			x -= 1


	def item_pager(self):
		self.item_far_left()
		for i in range(7):
			if self.item_loader() == False:
				move_and_click(self.item_right_arrow, 1)
			else:
				return
		print("No items in designated list found, using default")
		self.item_far_left()
		move_and_click(self.item_first_slot, 1)


	def item_loader(self):
		found = False
		for item in self.item_list:
			dir_path = '{}{}/'.format(self.item_dir, item)
			img_obj_list = self.load_image_from_dir(dir_path)
			print("Looking for {} using {} images".format(item, len(img_obj_list)))
			for img_obj in img_obj_list:
				get_item = self.find_item(item, img_obj)
				if get_item == False:
					pass
				else:
					move_and_click(get_item, 1)
					return
		print("Didn't find any images at all, go to next page")
		return found


	def find_item(self, item_name, item_obj):
		x, y, w, h = self.brawl_item_screen
		self.get_image(x, y, w, h, 'brawl_item')
		img = item_obj
		screen = cv2.imread('tmp_brawl_item.png')
		try:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.95)
			if fres[0].size == 0:
				#print("Did not find {}. Try finding another".format(item_name))
				return False
			elif fres[0].size > 1:
				cord = (fres[1][0]+x, fres[0][0]+y)
				print("Found {} @ {}, {}. Placing Bet!".format(item_name, cord[0], cord[1]))
				return cord
			elif fres[0].size == 1:
				cord = (fres[1]+x, fres[0]+y)
				print("Found {} @ {}, {}. Placing Bet!".format(item_name, cord[0], cord[1]))
				return cord
		except:
			print("Did not find item.")
			move_and_click(self.close_pos, 1)		


	def find_equipment(self, equipment, item_obj):
		x, y, w, h = self.brawl_item_screen
		self.get_image(x, y, w, h, 'brawl_equip')
		img = item_obj
		screen = cv2.imread('tmp_brawl_equip.png')
		try:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.90)
			if fres[0].size == 0:
				return False
			elif fres[0].size > 1:
				cord = (fres[1][0]+x, fres[0][0]+y)
				print("Found {} @ {}, {}. Equipping!".format(equipment, cord[0], cord[1]))
				return cord
			elif fres[0].size == 1:
				cord = (fres[1]+x, fres[0]+y)
				print("Found {} @ {}, {}. Equipping!".format(equipment, cord[0], cord[1]))
				return cord
		except:
			print("Did not find equipment.")
			move_and_click(self.close_pos, 1)


	def equipper(self):
		x, y, w, h = self.brawl_screen
		ct = curr_time()
		move_and_click(self.decline_confirm, 1)
		self.get_image()
		#self.get_image(x, y, w, h, ct)
		img_obj_list = self.load_image_from_dir('../templates/brawl/empty_equip/')
		screen = cv2.imread('tmp_brawl.png')
		for img in img_obj_list:
			try:
				result = cv2.matchTemplate(screen, img, method) # Does it match?
				fres = np.where(result >= 0.80)
				if fres[0].size == 0:
					pass
				elif fres[0].size > 1:
					cord = (fres[1][0]+x, fres[0][0]+y)
					print("Found empty equipment @ {}, {}. Equipping...".format(cord[0], cord[1]))
					return(cord)
				elif fres[0].size == 1:
					cord = (fres[1]+x, fres[0]+y)
					print("Found empty equipment @ {}, {}. Equipping...".format(cord[0], cord[1]))
					return(cord)
			except:
				print("Something failed in equipper!")
		print("Looks like all brawlers have equipment, go brawl!")
		return False


	def equip_villager(self):
		x, y, w, h = self.brawl_item_screen
		equip = self.equipper()
		if equip == False:
			return
		else:
			move_and_click(equip, 1) # click open weapon slot
			self.get_image(x, y, w, h, 'brawl_equip')
			self.equip_pager()


	def equip_pager(self):
		self.item_far_left()
		for i in range(7):
			if self.equip_loader() == False:
				move_and_click(self.item_right_arrow, 1)
			else:
				return
		print("No items in designated list found, using none")


	def equip_loader(self):
		found = False
		for equipment in self.equipment_list:
			dir_path = '{}{}/'.format(self.equipment_dir, equipment)
			img_obj_list = self.load_image_from_dir(dir_path)
			print("Looking for {} using {} images".format(equipment, len(img_obj_list)))
			for img_obj in img_obj_list:
				get_equipment= self.find_equipment(equipment, img_obj)
				if get_equipment == False:
					pass
				else:
					move_and_click(get_equipment, 1)
					print("Found an item: {}".format(equipment))
					move_and_click(self.decline_confirm, 1)
					self.equip_villager()
					return
		print("Didn't find any images at all, go to next page")
		return found


	def squad_fight(self, squad_name):
		move_and_click(self.next_opp, 1)
		for brawler in squad_name: # Click the brawlers
			move_and_click(brawler, 2)
		move_and_click(self.decline_confirm, 1)
		self.equip_villager()
		move_and_click(self.place_bet_pos, 1) # Click Bet Button
		self.item_pager()
		move_and_click(self.first_pot_pos, 1) # Open first potion box
		move_and_click(self.first_pot_pos, 1) # Select first potion in list
		move_and_click(self.close_item_pos, 1) # Cursory potion box close in case no potions
		move_and_click(self.fight_pos, 1) # Fight
		move_and_click(self.remove_shield, 1) # Remove shield
		move_and_click(self.skip_pos, 1) # skip
		move_and_click(self.skip_pos, 1) # Collect
		move_and_click(self.decline, 1) # Collect
		move_and_click(self.decline_confirm, 1) # Collect
		move_and_click(self.cancel_recovery, 1) # Collect
		time.sleep(5)


	def squad_generator(self):
		available = self.whose_available()
		out_squad = []
		if len(available) >= 3:
			out_squad.append(self.villager_gettr(available[0]))
			out_squad.append(self.villager_gettr(available[1]))
			out_squad.append(self.villager_gettr(available[2]))
			available.pop(0)
			available.pop(0)
			available.pop(0)
			print(out_squad)
			return out_squad
		else:
			print("Not enough players for a squad!")
			return False


	def org_fight(self):
		refresh_checker()
		if self.all_available():
			for squad in self.squad_list:
				refresh_check()
				self.squad_fight(squad)
		else:
			while len(self.whose_available()) >= 3:
				tmp_squad = self.squad_generator()
				self.squad_fight(tmp_squad)
				self.whose_available()
		move_and_click(self.close_pos, 1)


	def test_fight(self):
		self.open_ring()
		self.squad_fight(self.squad_loser)
		#move_and_click(self.close_pos, 1)


if __name__ == '__main__':
	#zoom_out()
	#time.sleep(1)
	move_and_click((828, 41),1)
	b = Brawl()
	b.org_fight()

