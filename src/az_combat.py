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

mouse = Controller()

# Logging #
LOG_FORMAT = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(filename = "/opt/dev/az/log/combat.log", 
					level=logging.INFO,
					format=LOG_FORMAT)
logger = logging.getLogger()


method =  cv2.TM_CCOEFF_NORMED

enemy_template_folder = '/opt/dev/az/templates/combat/enemies/'
combat_page_check_img = '/opt/dev/az/templates/combat/combat_page_check_2.png'
load_enemies = os.listdir(enemy_template_folder)
enemies_loaded = []
for enemy in load_enemies:
	enemy_tmp = cv2.imread(enemy_template_folder+enemy)
	enemies_loaded.append(enemy_tmp)

attack_screen_dimensions = ()


class Combat():
	def __init__(self):
		self.screen_w = 1256
		self.screen_h = 920
		self.x = 70
		self.y = 140
		self.ch = CordHelper()
		self.enemies = self.load_images_from_dir('/opt/dev/az/templates/combat/enemies/')
		self.team = self.load_images_from_dir('/opt/dev/az/templates/combat/team/')

	def load_images_from_dir(self, dirname):
		out_list = []
		file_list = os.listdir(dirname)
		for img in file_list:
			img_tmp = cv2.imread(dirname+img)
			out_list.append(img_tmp)
		return out_list


	def show_screen(self):
		segment = np.array(ImageGrab.grab(bbox=(self.x, self.y, self.x+self.screen_w, self.y+self.screen_h)))
		cv2.namedWindow("main", cv2.WINDOW_NORMAL)
		cv2.resizeWindow('main', int(self.screen_w/1.91), int(self.screen_h/1.91))
		cv2.imshow('main', cv2.cvtColor(np.array(segment), cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25) & 0xFF==ord('q'):
			cv2.destroyAllWindows()
			sys.exit()


	def combat_page_check(self):
		cpc = cv2.imread(combat_page_check_img)
		self.get_screen('tmp_cpc.png', True)
		screen = cv2.imread('tmp_cpc.png')
		try:
			result = cv2.matchTemplate(screen, cpc, method)
			fres = np.where(result >= 0.8)
			if len(fres[0])>0 and len(fres[1])>0:
				logger.info("Found Combat Page, continuing to battle")
				os.remove('tmp_cpc.png')
				return True
			else:
				logger.warning("Combat page not open")
				os.remove('tmp_cpc.png')
				return False
		except:
			logger.critical("Combat images faulty, check input images")
			os.remove('tmp_cpc.png')
			raise Exception("Combat images faulty, check input images")


	def get_combat_page_cord(self):
		cpc = cv2.imread(combat_page_check_img)
		np.array(self.get_screen('tmp_cpc.png', True))
		screen = cv2.imread('tmp_cpc.png')
		try:
			result = cv2.matchTemplate(screen, cpc, method)
			fres = np.where(result >= 0.95)
			if len(fres[0])>0 and len(fres[1])>0:
				cord = (int((self.x+fres[1])+10), int((self.y+fres[0])+10))
				logger.info("Combat Page Cords: {}".format(cord))
				os.remove('tmp_cpc.png')
				return cord
			else:
				logger.warning("Combat page not open")
				os.remove('tmp_cpc.png')
				return False
		except:
			logger.critical("Combat images faulty, check input images")
			os.remove('tmp_cpc.png')
			raise Exception("Combat images faulty, check input images")


	def get_screen(self, fn='tmp.png', save=False):
		segment = ImageGrab.grab(bbox=(self.x, self.y, self.screen_w, self.screen_h))
		if save:
			segment.save(fn, 'PNG')
		return segment


	def get_screen_segment(self, name, x, y, w, h):
		segment = ImageGrab.grab(bbox=(x, y, x+w, y+h))
		segment.save(name, 'PNG')
		return segment
		

	def find_enemies_from_template(self, screen='', enemy=''):
		if str(enemy) == '':
			enemy = cv2.imread(enemy_template_folder+'enemy_large_1.png')
		if str(screen) == '':
			self.get_screen('tmp_find.png', True)
			screen = cv2.imread('tmp_find.png')
		else:
			screen = cv2.imread('tmp_find.png')
		result = cv2.matchTemplate(screen, enemy, method)
		fres = np.where(result >= 0.80)
		c_list = self.ch.optimise_cord(fres, 20, 100)
		return c_list

	
	def find_all_enemies(self, template_list, screen=''):
		if screen == '':
			self.get_screen('tmp_find.png', True)
			screen = cv2.imread('tmp_find.png')
		cord_list = []
		for img in template_list:
			data = self.find_enemies_from_template(screen, img)
			for i in data:
				cord_list.append(i)
		return cord_list


	def correct_cords(self, cord, x_off, y_off):
		x, y = cord
		x = (x+x_off)
		y = (y+y_off)
		return (x, y)


	def get_atk_screen(self, cord):
		#cord = self.get_combat_page_cord()
		#cord = self.correct_cords(cord, 2, self.x, self.y)
		x = cord[0]
		y = cord[1]
		x_s = x-240
		y_s = y
		try:
			atk_screen = self.get_screen_segment('tmp_atk_screen.png',x_s, y_s, 600, 400)
			return atk_screen
		except:
			print("Couldn't get attack screen")
			return False
		

	def click_pac(self, combat_cord):
		x_m = 67
		x, y = combat_cord
		x_s = x-90
		y_s = y+320
		mousePos((x_s, y_s))
		time.sleep(0.2)
		mousePos((x_s, y_s))
		time.sleep(0.2)
		move_and_click((x_s, y_s))
		time.sleep(0.2)
		count = 1
		ctw = False
		while ctw == False:
			x_s += x_m
			mousePos((x_s, y_s))
			time.sleep(0.2)
			mousePos((x_s, y_s))
			time.sleep(0.2)
			refresh_checker()
			move_and_click((x_s, y_s))
			time.sleep(0.2)
			count += 1
			ctw = self.get_ctw(combat_cord)
		attack_button_x = x+64
		attack_button_y = y+430
		attack_button_pos = (x+64, y+430)
		mousePos(attack_button_pos)
		time.sleep(0.2)
		mousePos(attack_button_pos)
		time.sleep(0.2)
		mousePos(attack_button_pos)
		time.sleep(0.2)
		move_and_click(attack_button_pos)
		time.sleep(0.2)
		move_and_click(attack_button_pos)
		time.sleep(0.2)


	def get_ctw(self, cord):
		""" return true if ctw is 100% """
		self.get_atk_screen(cord)
		segment = cv2.imread('tmp_atk_screen.png')
		template = cv2.imread('ctw_2.png')
		result = cv2.matchTemplate(segment, template, method)
		fres = np.where(result >= 0.9)
		if len(fres[0]) >= 1:
			print("Attack!")
			return True
		else:
			#print("Not ready to engage yet!")
			return False


	def clear_enemies(self, enemy_list):
		#print(enemy_list)
		for enemy in enemy_list:
			self.engage_enemy(enemy)
			time.sleep(10)
			new_el = self.find_all_enemies(self.enemies)
			self.clear_enemies(new_el)


	def engage_enemy(self, enemy_cord):
		enemy_cord = self.correct_cords(enemy_cord, self.x, self.y)
		move_and_click(enemy_cord) #click enemy
		if self.combat_page_check():
			cord = self.get_combat_page_cord()
			logger.info("Found Enemy and combat view open, ready to combat")
			self.get_atk_screen(cord)
			self.click_pac(cord)
		else:
			c_l = self.find_all_enemies(self.enemies)
			self.clear_enemies(c_l)



class Legion():
	def __init__(self):
		self.screen_w = 2570
		self.screen_h = 2075
		self.x = 0
		self.y = 325
		self.ch = CordHelper()
		self.team = self.load_images_from_dir('/opt/dev/az/templates/combat/team/')
		self.attack_arrow = self.load_image('/opt/dev/az/templates/combat/legion/red_arrow.png')
		self.map_pos = (-17, 897)


	def load_images_from_dir(self, dirname):
		out_list = []
		file_list = os.listdir(dirname)
		for img in file_list:
			img_tmp = cv2.imread(dirname+img)
			out_list.append(img_tmp)
		return out_list


	def load_image(self, img_path):
		img_tmp = cv2.imread(img_path)
		return img_tmp


	def find_attacker(self, screen=''):
		if str(screen) == '':
			self.get_screen('tmp_find.png', True)
			screen = cv2.imread('tmp_find.png')
		else:
			screen = cv2.imread('tmp_find.png')
		result = cv2.matchTemplate(screen, self.attack_arrow, method)
		fres = np.where(result >= 0.8)
		c_list = self.ch.optimise_cord(fres, 20, 100)
		print("Found Legion Attack @ {}".format(c_list[0]))
		return c_list


	def get_screen(self, fn='tmp.png', save=True):
		segment = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.screen_w, self.y+self.screen_h))
		if save:
			segment.save(fn, 'PNG')
		return segment


	def get_screen_segment(self, name, x, y, w, h):
		segment = ImageGrab.grab(bbox=(x, y, x+w, y+h))
		segment.save(name, 'PNG')
		return segment	


	def get_village_screen(self):
		x_s = 800
		y_s = 400
		village_screen = self.get_screen_segment('village.png',x_s, y_s, 240*2, 240*2)
		return village_screen


def clear_segment():
	cm = Combat()
	c_l = cm.find_all_enemies(cm.enemies)
	cm.clear_enemies(c_l)


def clear_all_enemies():
	print("Clearing Enemies in Top Left!")
	navy('top_left', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Left!")
	navy('bottom_left', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Middle!")
	navy('bottom_left', 6)
	move_screen_right(2, 300)
	clear_segment()
	print("Clearing Enemies in Middle Middle!")
	navy('bottom_left', 6)
	move_screen_right(2, 300)
	move_screen_up(4, 300)
	clear_segment()
	print("Clearing Enemies in Top Right!")
	navy('top_right', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Right!")
	navy('bottom_right', 6)
	clear_segment()


if __name__ == '__main__':
	move_and_click((688, 123)) # Focus Chrome frame!
	clear_all_enemies()


