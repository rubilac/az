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

start = 0.89
n = 5


screen = cv2.imread('gray-default.png')
item = cv2.imread('../templates/inventory/items/iron scraps.png')
result = cv2.matchTemplate(screen, item, method) # Load current screen

while n > 0:
	fres = np.where(result >= start)
	print(start, fres)
	start -= 0.01
	n -= 1