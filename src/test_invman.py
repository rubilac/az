# test_invman.py
import os
import unittest
from az_invman import Inventory
from az_invman import *
import shutil


testfile = '/opt/dev/az/test/test_fixtures/test_items_current_set_bak.json'
assertfile = '/opt/dev/az/test/test_fixtures/test_items_current_set.json'
emptyfile = '/opt/dev/az/test/test_fixtures/test_items_empty.json'
test_inv_gray = '/opt/dev/az/test/test_images/test_inv_gray.png'
test_brawl_color = '/opt/dev/az/test/test_images/test_brawl_color.png'
test_bt_bl_gray = '/opt/dev/az/test/test_images/test_bt_bl_gray.png'
emptyfilebak = '/opt/dev/az/test/test_fixtures/test_items_empty_bak.json'

shutil.copyfile(emptyfile, emptyfilebak)


class TestInv(unittest.TestCase):
	
	
	def test_open_bag_check_bag_is_open(self):
		test_inv = Inventory()
		cord = test_inv.open_bag_check(test_inv_gray)
		assert(type(cord)==tuple)
		assert(cord==(551, 426))


	def test_open_bag_check_bag_is_not_open(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			cord = test_inv.open_bag_check(test_brawl_color)
	

	def test_open_bag_check_invalid_input_file(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			cord = test_inv.open_bag_check('invalid_file')


	def test_open_bag_bag_is_open(self):
		test_inv = Inventory()
		cord = test_inv.open_bag(test_bt_bl_gray, 0.88)
		assert(cord==(1173, 1011))
		assert(type(cord)==tuple)


	def test_open_bag_threshold_too_strict(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			cord = test_inv.open_bag(test_bt_bl_gray, 0.9)


	def test_open_bag_threshold_too_lax(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			cord = test_inv.open_bag(test_bt_bl_gray, 0.5)


	def test_open_bag_bag_is_not_open(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			cord = test_inv.open_bag_check(test_brawl_color)


	def test_reset_counter(self):
		test_inv = Inventory()
		shutil.copyfile(assertfile, testfile)
		reset = test_inv.reset_counter(testfile)
		test_data = load_file(testfile)
		assert_data = load_file(assertfile)
		assert(reset==True)
		assert(test_data['il'][0]['item_count_cur'] == 0)
		assert(test_data['il'][0]['item_count_prev'] == assert_data['il'][0]['item_count_cur'])
		os.remove(testfile)


	def test_reset_counter_empty_file(self):
		test_inv = Inventory()
		with self.assertRaises(Exception):
			reset = test_inv.reset_counter(emptyfile)


	def test_get_image_default_minumum(self):
		test_inv = Inventory()
		image_int = test_inv.get_image(1, 1, 2, 2)
		assert(type(image_int)==int)
		assert(image_int >= 27 or image_int <= 40)


	def test_get_image_set_tag_save_true(self):
		test_inv = Inventory()
		image_int = test_inv.get_image(1, 1, 2, 2, "test_tag", True)
		assert(type(image_int)==int)
		assert(image_int >= 27 or image_int <= 40)
		path = '/opt/dev/az/src/'
		img_list = []
		for i in os.listdir(path):
			if os.path.isfile(os.path.join(path,i)) and 'test_tag' in i:
				img_list.append(i)
		assert(len(img_list)>0)
		for i in os.listdir(path):
			if os.path.isfile(os.path.join(path,i)) and 'test_tag' in i:
				os.remove(i)


	def test_get_color_image_default_minumum(self):
		test_inv = Inventory()
		image_int = test_inv.get_color_image(1, 1, 2, 2)
		assert(type(image_int)==int)
		assert(image_int >= 330 or image_int <= 400)


	def test_get_color_image_set_tag_save_true(self):
		test_inv = Inventory()
		image_int = test_inv.get_color_image(1, 1, 2, 2, "test_tag", True)
		assert(type(image_int)==int)
		assert(image_int >= 330 or image_int <= 400)
		path = '/opt/dev/az/src/'
		img_list = []
		for i in os.listdir(path):
			if os.path.isfile(os.path.join(path,i)) and 'test_tag' in i:
				img_list.append(i)
		assert(len(img_list)>0)
		for i in os.listdir(path):
			if os.path.isfile(os.path.join(path,i)) and 'test_tag' in i:
				os.remove(i)


	def test_add_item_to_store(self):
		test_int = 1
		test_inv = Inventory()
		shutil.copyfile(assertfile, testfile)
		add = test_inv.add_item_to_store(test_int, testfile)
		testfiledata = load_file(testfile)
		for i in testfiledata['il']:
			if i['item_int'] == test_int:
				assert(i['item_name'] == 'replace_me')
		assert(len(testfiledata['il'])>1)
		os.remove(testfile)


	def test_add_item_to_store_empty_file(self):
		test_int = 1
		test_inv = Inventory()
		with self.assertRaises(Exception):
			add = test_inv.add_item_to_store(test_int, emptyfilebak)


	def test_update_item_count(self):
		test_int = 1
		test_inv = Inventory()
		shutil.copyfile(assertfile, testfile)
		add = test_inv.add_item_to_store(test_int, testfile)
		update = test_inv.update_item_count(test_int, testfile)
		update = test_inv.update_item_count(test_int, testfile)
		testfiledata = load_file(testfile)
		for i in testfiledata['il']:
			if i['item_int'] == test_int:
				assert(i['item_name'] == 'replace_me')

				assert(i['item_count_cur'] == 2)
		assert(len(testfiledata['il'])>1)
		os.remove(testfile)


	def test_update_item_count_empty_file(self):
		test_int = 1
		test_inv = Inventory()
		with self.assertRaises(Exception):
			update = test_inv.update_item_count(test_int, emptyfilebak)


	def test_img_in_store_img_exists(self):
		test_int = 1
		test_inv = Inventory()
		shutil.copyfile(assertfile, testfile)
		add = test_inv.add_item_to_store(test_int, testfile)
		data = test_inv.img_in_store(test_int, testfile)
		assert(type(data)==dict)
		assert(data['item_int']==1)
		assert(data['item_count_cur']==0)
		os.remove(testfile)


	def test_img_in_store_img_no_exists(self):
		test_int = 2
		test_inv = Inventory()
		shutil.copyfile(assertfile, testfile)
		data = test_inv.img_in_store(test_int, testfile)
		testfiledata = load_file(testfile)
		for i in testfiledata['il']:
			if i['item_int'] == test_int:
				assert(i['item_name'] == 'replace_me')
		assert(len(testfiledata['il'])>1)
		os.remove(testfile)


	def test_inv_slot_gen(self):
		test_inv = Inventory()
		pass


	def test_get_inv_slots(self):
		#bag_cord = 0
		#test_inv = Inventory()
		#test_inv.get_inv_slots(bag_cord)
		pass


if __name__=='__main__':
   	unittest.main(exit=False)
