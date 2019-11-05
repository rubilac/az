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
from az_imaging import *
import toml
config = toml.load('.config')

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

in_village_img_path = config['zones']['in_village_img_path']
out_village_img_path = config['zones']['out_village_img_path']
egypt_img_path = config['zones']['egypt_img_path']

class Combat():
	def __init__(self):
		self.screen_w = 1488
		self.screen_h = 925
		self.x = 70
		self.y = 160
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
				#os.remove('tmp_cpc.png')
				return True
			else:
				logger.warning("Combat page not open")
				#os.remove('tmp_cpc.png')
				return False
		except:
			logger.critical("Combat images faulty, check input images")
			#os.remove('tmp_cpc.png')
			raise Exception("Combat images faulty, check input images")


	def get_combat_page_cord(self):
		cpc = cv2.imread(combat_page_check_img)
		np.array(self.get_screen('tmp_cpc.png', True))
		screen = cv2.imread('tmp_cpc.png')
		try:
			result = cv2.matchTemplate(screen, cpc, method)
			fres = np.where(result >= 0.90)
			print(fres)
			if len(fres[0])>0 and len(fres[1])>0:
				slots = zip(fres[0], fres[1])
				slot_set = set(slots)
				tmp = list(slot_set)[0]
				cord = (int((self.x+tmp[1])+10), int((self.y+tmp[0])+10))
				#os.remove('tmp_cpc.png')
				return cord
			else:
				logger.warning("Combat page not open")
				#os.remove('tmp_cpc.png')
				return False
		except:
			logger.critical("Combat images faulty, check input images")
			#os.remove('tmp_cpc.png')
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
		print(cord)
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
		self.screen_w = 1488
		self.screen_h = 925
		self.x = 70
		self.y = 160
		self.ch = CordHelper()
		self.team = self.load_images_from_dir('/opt/dev/az/templates/combat/team/')
		self.attackers = self.load_images_from_dir('/opt/dev/az/templates/combat/legion/')
		self.village_pos = (1396, 880)
		self.strength_cords = (1288, 171, 1315, 190)
		self.strength_threshold = config['general']['strength']


	def load_images_from_dir(self, dirname):
		out_list = []
		file_list = os.listdir(dirname)
		for img in file_list:
			img_tmp = cv2.imread(dirname+img)
			out_list.append(img_tmp)
		return out_list


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


	def get_strength(self):
		segment_grab_custom(self.strength_cords, 'strength') #
		strength = int(get_num_from_image('segment_strength.jpg'))
		if strength > 170:
			print("Strenght read badly, failing...")
			return False
		else:
			print("********Strength is : {}".format(strength))
			return strength


	def get_combat_page_cord(self):
		cpc = cv2.imread(combat_page_check_img)
		np.array(self.get_screen('tmp_cpc.png', True))
		screen = cv2.imread('tmp_cpc.png')
		try:
			result = cv2.matchTemplate(screen, cpc, method)
			fres = np.where(result >= 0.90)
			if len(fres[0])>0 and len(fres[1])>0:
				slots = zip(fres[0], fres[1])
				slot_set = set(slots)
				tmp = list(slot_set)[0]
				cord = (int((self.x+tmp[1])+10), int((self.y+tmp[0])+10))
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
		count = 5
		ctw = False
		while count > 0:
			x_s += x_m
			mousePos((x_s, y_s))
			time.sleep(0.2)
			mousePos((x_s, y_s))
			time.sleep(0.2)
			refresh_checker()
			move_and_click((x_s, y_s))
			time.sleep(1)
			count -= 1
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
		time.sleep(10)
		refresh_checker()
		move_and_click(self.village_pos)


	def engage_attacker(self, enemy_cord):
		move_and_click(enemy_cord) #click enemy
		time.sleep(10)
		refresh_checker()
		cord = self.get_combat_page_cord()
		if cord != False:
			logger.info("Found Enemy and combat view open, ready to combat")
			self.get_atk_screen(cord)
			self.click_pac(cord)
		else:
			print("Something went wrong, oh no")


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
		

	def ready_to_attack(self):
		strength = self.get_strength()
		if strength >= self.strength_threshold:
			cord = self.find_attackers_from_template(self.attackers)
			if cord != False:
				cord = self.correct_cords(cord, 350, 250)
				self.engage_attacker(cord)
			else:
				pass
		else:
			print("Not strong enough yet! {}, I need {} to fight".format(strength, self.strength_threshold))
			pass


	def find_attackers_from_template(self, enemies, screen=''):
		print("Going to Village view, because we are strong enough to fight!")
		move_and_click(self.village_pos)
		if str(screen) == '':
			self.get_village_screen()
			screen = cv2.imread('village.png')
		else:
			screen = cv2.imread('village.png')
		for enemy in enemies:
			result = cv2.matchTemplate(screen, enemy, method)
			fres = np.where(result >= 0.95)
			if len(fres[0]) >= 1:
				print("Attacker found @ {} {}".format(fres[1][0], fres[0][0]))
				cord = (fres[1][0], fres[0][0])
				return cord
		print("No Attackers present, going back into town")
		move_and_click(self.village_pos)
		return False


	def correct_cords(self, cord, x_off, y_off):
		x, y = cord
		x = (x+x_off)
		y = (y+y_off)
		return (x, y)


	def load_image(self, img_path):
		img_tmp = cv2.imread(img_path)
		return img_tmp


	def match_template(self, screen, img, threshold=0.95, method=cv2.TM_CCOEFF_NORMED):
		result = cv2.matchTemplate(screen, img, method)
		fres = np.where(result >= threshold)
		return fres


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
		x_s = 350
		y_s = 250
		village_screen = self.get_screen_segment('village.png',x_s, y_s, 300, 200)
		return village_screen


class Zone():
	def __init__(self):
		self.screen_w = 1488
		self.screen_h = 925
		self.x = 70
		self.y = 160


	def match_template(self, screen, img, threshold=0.95, method=cv2.TM_CCOEFF_NORMED):
		result = cv2.matchTemplate(screen, img, method)
		fres = np.where(result >= threshold)
		return fres


	def get_screen(self, fn='tmp.png', save=True):
		segment = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.screen_w, self.y+self.screen_h))
		if save:
			segment.save(fn, 'PNG')
		return segment


	def where_am_i(self):
		""" 
			returns:
			1 - In Village
			2 - Out Village
			3 - Egypt
			4 - Error
		"""
		refresh_checker() # refresh_checker - Get rid of any popups
		nav_top_l(3) # reset position to top left
		zoom_out_max()
		self.get_screen() # full screen grab
		screen = cv2.imread('tmp.png')
		in_village = self.match_template(screen, cv2.imread(in_village_img_path))
		out_village = self.match_template(screen, cv2.imread(out_village_img_path))
		egypt = self.match_template(screen, cv2.imread(egypt_img_path))
		if len(in_village[0]) != 0:
			print("We are inside the village")
			return 1
		elif len(out_village[0]) != 0:
			print("We are outside the village")
			return 2
		elif len(egypt[0]) != 0:
			print("We are in Egypt")
			return 3
		else:
			zoom_out_max()
			print("Where the fuck are we?!")
			return 4



def clear_segment():
	cm = Combat()
	c_l = cm.find_all_enemies(cm.enemies)
	cm.clear_enemies(c_l)


def clear_all_enemies():
	print("Clearing Enemies in Top Left!")
	refresh_checker()
	navy('top_left', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Left!")
	refresh_checker()
	navy('bottom_left', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Middle!")
	refresh_checker()
	navy('bottom_left', 6)
	move_screen_right(2, 300)
	clear_segment()
	print("Clearing Enemies in Middle Middle!")
	refresh_checker()
	navy('bottom_left', 6)
	move_screen_right(2, 300)
	move_screen_up(4, 300)
	clear_segment()
	print("Clearing Enemies in Top Right!")
	refresh_checker()
	navy('top_right', 6)
	clear_segment()
	print("Clearing Enemies in Bottom Right!")
	refresh_checker()
	navy('bottom_right', 6)
	clear_segment()


def strength():
	lg = Legion()
	lg.ready_to_attack()
	cz = Zone()
	zone = cz.where_am_i()
	while zone != 1:
		refresh_checker()
		zoom_out_max()
		move_and_click(lg.village_pos)
		zone = cz.where_am_i()

def get_zone():
	cz = Zone()
	zone = cz.where_am_i()
	print(zone)


if __name__ == '__main__':
	move_and_click((763, 42))
	clear_all_enemies()
	strength()
	#get_zone()
	#zoom_out() # Focus Chrome frame!
	#cm = Legion()
	#cm.get_screen('tmp_find.png',True)
	#cm.where_am_i()
	#cord = (cm.get_combat_page_cord())
	#cm.get_atk_screen(cord)
