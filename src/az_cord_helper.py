import os
import sys
import time
import json
import datetime
import timeit
import cv2
import numpy as np
#from az_code import *


class CordHelper():
	def __init__(self, cord_list=0, b_x=0, b_y=0):
		from az_farmer import write_cords_optimised
		#print("manage cords")
		self.cord_list = 0
		self.b_x = 0
		self.b_y = 0


	def sort_list(unsorted_list):
		unsorted_list.sort(key=lambda tup: tup[1])
		return unsorted_list


	def remove_bounded_entries(self):
		out_list = []
		cord_list = self.sort_list(cord_list)
		for cord in cord_list:
			if len(out_list) == 0:
				prv_x = 0
				prv_y = 0
			x, y = cord
			if x > prv_x+b_x or x < prv_x-b_x or y > prv_y+b_y or y < prv_y-b_y:
				out_list.append(cord)
				prv_x, prv_y = cord
		return out_list


	def write_cords_to_file(self, img, cord_list, n):
		segment = cv2.imread(img)
		for cord in cord_list:
			cv2.circle(segment, (cord[0], cord[1]), 15, (0,0,255), -1)
		cv2.imwrite('final-{}.png'.format(n), segment)


	def optimise_cord(self, fres, x_b, x_y):
		c_list = []
		x_b = 100
		y_b = 20
		prv_x = 0
		prv_y = 0
		for i in (zip(*fres[::-1])):
			x = i[0]
			y = i[1]
			if x > prv_x+x_b or x < prv_x-x_b or y > prv_y+y_b or y < prv_y-y_b:
				c_list.append(i)
				prv_x = i[0]
				prv_y = i[1]
		return c_list


	def combined_cords(template_list, screengrab):
		cord_list = []
		c_list = []
		for img in template_list:
			data = write_cords_optimised(img)
			for i in data:
				cord_list.append(i)
		return cord_list



class ImageHelper():
	def __init__(self):
		self.refresh_screen = (689, 432, 874, 604)
		self.refresh_img = '/opt/dev/az/templates/popups/refresh.png'


	def get_screen(self, cord, tag, img_type=0, save=True):
		"""
			cord = (x, y, w, h)
			type = 'gray' or 'colour'
			save = True or False
		"""
		try:
			x, y, w, h = cord
		except:
			print("Cords not in the correct format requires (x, y, w, h)")
		out_img = "{}.png".format(tag)
		try:
			if img_type == 0:
				im = ImageOps.grayscale(ImageGrab.grab(cord))
				im.save(out_img, 'PNG')
				params = ['mogrify', out_img, out_img]
				subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
			elif img_type == 1:
				im = ImageGrab.grab(cord)
				im.save(out_img, 'PNG')
				params = ['mogrify', out_img, out_img]
				subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
			else:
				print("img_type needs to be gray or colour")
				return
		except:
			print("Get screen failed")


	def rc(self, i='/opt/dev/az/templates/popups/refresh.png', s='tmp_refresh.png', method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
		self.get_screen((690, 432, 870, 604), 'tmp_refresh', 1)
		img = cv2.imread(i)
		screen = cv2.imread(s)
		try:
			result = cv2.matchTemplate(screen, img, method)
			fres = np.where(result >= threshold)
			if len(fres[0])>0 and len(fres[1])>0:
				slots = zip(fres[1], fres[0])
				slot_set = set(slots)
				#print(list(slot_set)[0])
				return list(slot_set)[0]
			else:
				print("No matches found!")
				return False
		except:
			raise Exception("Input images faulty!")


def info():
	import timeit
	num = 100
	t = timeit.timeit("ih = ImageHelper()\nih.rc()", setup="from __main__ import ImageHelper\nimport cv2\nimport numpy as np", number=num)
	print("Took {}s to match {} times. {}ms per full cord return".format(round(t,2), num, round(t/num*1000, 2)))


def profiler():
	import timeit
	num = 100
	t = timeit.timeit("ih.get_screen((689, 432, 874, 604), 'tmp_refresh_colour', 1)", setup="from __main__ import ImageHelper\nih = ImageHelper()", number=num)
	g = timeit.timeit("ih.get_screen((689, 432, 874, 604), 'tmp_refresh_gray', 0)", setup="from __main__ import ImageHelper\nih = ImageHelper()", number=num)
	i = timeit.timeit("i = cv2.imread(img)", setup="import cv2\nimg = '/opt/dev/az/templates/popups/refresh.png'", number=num)
	s = timeit.timeit("s = cv2.imread(screen)", setup="import cv2\nscreen = 'tmp_refresh.png'", number=num)
	m = timeit.timeit("result = cv2.matchTemplate(s, i, method)", setup="import cv2\ns = cv2.imread('tmp_refresh.png')\ni = cv2.imread('/opt/dev/az/templates/popups/refresh.png')\nmethod = cv2.TM_CCOEFF_NORMED", number=num)
	f = timeit.timeit("fres = np.where(result >= 0.9)", setup="import cv2\nimport numpy as np\ns = cv2.imread('tmp_refresh.png')\ni = cv2.imread('/opt/dev/az/templates/popups/refresh.png')\nmethod = cv2.TM_CCOEFF_NORMED\nresult = cv2.matchTemplate(s, i, method)", number=num)

	print("Took {}s to get colour screen {} times. {}ms per get".format(round(t,2), num, round(t/num*1000, 2)))
	print("Took {}s to get gray screen {} times. {}ms per get".format(round(g,2), num, round(g/num*1000, 2)))
	print("Took {}s to import refresh img {} times. {}ms per get".format(round(i,2), num, round(i/num*1000, 2)))
	print("Took {}s to import refresh img {} times. {}ms per get".format(round(s,2), num, round(s/num*1000, 2)))
	print("Took {}s to match img to screen {} times. {}ms per match".format(round(m,2), num, round(m/num*1000, 2)))
	print("Took {}s to match above threshold {} times. {}ms per match".format(round(f,2), num, round(f/num*1000, 2)))


if __name__ == '__main__':
	pass

