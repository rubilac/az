import os
import sys
import time
import json
import datetime
from az_code import *
from az_farmer import *
import pyscreenshot as ImageGrab
from PIL import ImageOps
from numpy import *
import pynput.mouse as ms
import pynput.keyboard as kb
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
import numpy as np
import cv2
import shutil
import logging


def get_image(x=70, y=100, width=1470, length=927, tag="default"):
	"""
		Given x, y cords and width and length size, take a grayscale image and return the
		summed value.
		Option to save the image is off by default.
	"""
	box = (x, y, width, length)
	im = ImageGrab.grab(box)
	#ts = int(time.time())
	fn = "color-{}.png".format(tag)
	im.save(fn,'PNG')
	params = ['mogrify', fn, fn]
	subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
	logger.info("Saved image: {}".format(fn))


#get_image()
screen = cv2.imread('gray-default.png')
item = cv2.imread('/opt/dev/az/templates/inventory/items/boar skins.png')
method = cv2.TM_CCORR_NORMED
slot_list = []


result = cv2.matchTemplate(screen, item, method) # Load current screen
fres = np.where(result >= 0.99)
print(fres)
slots = zip(fres[0], fres[0])
print(slots)
slot_set = set(slots)
#print(slot_set)
count = 0
for i in slot_set:
	count += 1
	slot_list.append(i)
out = [slot_list, count]
print(out)