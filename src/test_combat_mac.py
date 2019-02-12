# test_invman.py
import os
import unittest
from az_combat_mac import Combat
from az_cord_helper import CordHelper
from os.path import join
import shutil
import cv2

template_path_combat = '/opt/dev/az/templates/combat/'
testfile = '/opt/dev/az/test/test_fixtures/test_items_current_set_bak.json'
load_enemies = os.listdir(template_path_combat)
enemies_loaded = []


for enemy in load_enemies:
	enemy_tmp = cv2.imread(template_path_combat+enemy)
	enemies_loaded.append(enemy_tmp)
#shutil.copyfile(emptyfile, emptyfilebak)

#		with self.assertRaises(Exception):
#			cord = test_inv.open_bag_check(test_brawl_color)
class TestCombat(unittest.TestCase):
	
	
	def test_find_enemies_from_template(self):
		tc = Combat()
		c_l = tc.find_enemies_from_template('','')
		print(c_l)
		assert(type(c_l)==list)
		assert(type(c_l[0])==tuple)
		assert(c_l[0]==(2153, 681))
		#assert(c_l[1]==(2167, 1993))
	

	def test_combined_cords(self):
		tc = Combat()
		cc = tc.find_all_enemies(enemies_loaded, '/opt/dev/az/test/test_images/test_combat_enemy_finder.png')
		print(cc)
		assert(type(cc)==list)
		assert(type(cc[0])==tuple)
		assert(cc[0]==(2153, 681))
		assert(cc[1]==(2167, 1993))


if __name__=='__main__':
   	unittest.main(exit=False)
