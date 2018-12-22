from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime
from az_code import *
from PIL import ImageOps
from numpy import *


def click_menu(timer=2):
	move_and_click((995,941), timer)


def click_punch(timer=2):
	move_and_click((1408,916), timer)


def click_stop(timer):
	move_and_click((1384,947), timer)


def get_rewards(timer):
	move_and_click((1135,935), timer)

def punch():
	click_menu()
	click_punch()
	click_stop(1.6)
	click_stop(2)
	click_stop(3.05)
	click_stop(3.1)
	time.sleep(40)
	get_rewards(4)
	get_rewards(4)
	get_rewards(4)


if __name__ == '__main__':
	n = 30
	while n > 0:
		punch()
		n -= 1
	#output_cords()