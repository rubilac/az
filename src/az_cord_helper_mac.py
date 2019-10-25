import os
import sys
import time
import json
import datetime
from az_code_mac import *
from az_farmer_mac import *


class CordHelper():
	def __init__(self, cord_list=0, b_x=0, b_y=0):
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


if __name__ == '__main__':	
	pass