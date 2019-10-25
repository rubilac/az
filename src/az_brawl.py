#az_brawl

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

method =  cv2.TM_CCOEFF_NORMED

class Brawl():
	def __init__(self):
		self.ring_pos = (902, 350)
		self.challenge = (926, 286)
		self.brawl_screen = (400, 300, 1150, 730)
		self.brawl_item_screen = (580, 390, 970, 670)
		self.place_bet_pos = (777, 513)
		self.fight_pos = (775, 705)
		self.skip_pos = (775, 705)
		self.close_pos = (1123, 332)
		self.close_item_pos = (988, 397)
		self.remove_shield = (849, 596)
		# Brawlers
		self.worker = (562, 586)
		self.edifis = (645, 584)
		self.ekonomikrisis = (746, 587)
		self.pointandclix = (811, 586)
		self.lunatix = (903, 584)
		self.democratix = (994, 583)
		self.ironix = (562, 653)
		self.baltix = (658, 651)
		self.lyrix = (738, 650)
		# Squads
		self.num_b = config['brawl']['num_brawlers']
		if self.num_b == 9:
			self.squad_1 = [self.pointandclix, self.worker, self.lunatix]
			self.squad_2 = [self.ekonomikrisis, self.ironix, self.lyrix]
			self.squad_3 = [self.edifis, self.democratix, self.baltix]
			self.squad_list = [self.squad_1, self.squad_2, self.squad_3]
		elif self.num_b == 8:
			self.squad_1 = [self.pointandclix, self.worker, self.baltix]
			self.squad_2 = [self.edifis, self.ironix, self.democratix]
			self.squad_list = [self.squad_1, self.squad_2]
		self.squad_loser = [self.lunatix, self.lyrix, self.baltix]	
		# Potions
		self.first_pot_pos = (689, 478)


	def open_ring(self):
		nav_to_town()
		move_and_click(self.ring_pos, 1)
		move_and_click(self.challenge, 1)


	def get_image(self, x=400, y=300, width=1150, length=730, tag="brawl"):
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


	def all_available(self):
		self.open_ring()
		time.sleep(5)
		self.get_image()
		if self.num_b == 9:
			img = cv2.imread('../templates/brawl/all_available.png')
		elif self.num_b == 8:
			img = cv2.imread('../templates/brawl/8_available.png')
		else:
			print("Which image?")
			return
		screen = cv2.imread('tmp_brawl.png')
		try:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.95)
			if fres[0].size == 0:
				print("Not all brawlers available! try again later")
				move_and_click(self.close_pos, 1)
				return 1
			elif fres[0].size >= 1:
				print("All brawlers available, lets go")
				return True
		except:
			print("Not all brawlers available! try again later")
			move_and_click(self.close_pos, 1)


	def find_item(self):
		x, y, w, h = self.brawl_item_screen
		self.get_image(x, y, w, h, 'brawl_item')
		img = cv2.imread('../templates/brawl/coal.png')
		screen = cv2.imread('tmp_brawl_item.png')
		try:
			result = cv2.matchTemplate(screen, img, method) # Does it match?
			fres = np.where(result >= 0.95)
			if fres[0].size == 0:
				print("Did not find Coal. Using first position")
				move_and_click((653, 460), 1)
				return False
			elif fres[0].size > 1:
				cord = (fres[1][0]+x, fres[0][0]+y)
				print("Found Coal @ {}, {}. Placing Bet!".format(cord[0], cord[1]))
				return cord
			elif fres[0].size == 1:
				cord = (fres[1]+x, fres[0]+y)
				print("Found Coal @ {}, {}. Placing Bet!".format(cord[0], cord[1]))
				return cord
		except:
			print("Did not find item.")
			move_and_click(self.close_pos, 1)		



	def squad_fight(self, squad_name):
		for brawler in squad_name: # Click the brawlers
			move_and_click(brawler, 2)
		move_and_click(self.place_bet_pos, 1) # Click Bet Button
		get_coal = self.find_item()
		if get_coal == False:
			pass
		else:
			move_and_click(get_coal, 1) # Get and Click Coal
		move_and_click(self.first_pot_pos, 1) # Open first potion box
		move_and_click(self.first_pot_pos, 1) # Select first potion in list
		move_and_click(self.close_item_pos, 1) # Cursory potion box close in case no potions
		move_and_click(self.fight_pos, 1) # Fight
		move_and_click(self.remove_shield, 1) # Remove shield
		move_and_click(self.skip_pos, 1) # skip
		move_and_click(self.skip_pos, 1) # Collect
		time.sleep(5)

	def org_fight(self):
		refresh_checker()
		if self.all_available():
			for squad in self.squad_list:
				refresh_check()
				self.squad_fight(squad)
			move_and_click(self.close_pos, 1)
		else:
			print("Come back later, not everyone is available")
			return

	def test_fight(self):
		refresh_checker()
		self.open_ring()
		self.squad_fight(self.squad_loser)
		move_and_click(self.close_pos, 1)


if __name__ == '__main__':
	b = Brawl()
	b.org_fight()
