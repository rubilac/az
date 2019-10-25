import pyscreenshot as ImageGrab
import os
import time
import json
import datetime
import sys
import cv2
from az_code import *
from PIL import ImageOps
import numpy as np



def show_screen_gray():
	segment = np.array(ImageOps.grayscale(ImageGrab.grab(bbox=(400, 400, 950, 700))))
	cv2.namedWindow("main", cv2.WINDOW_NORMAL)
	cv2.resizeWindow('main', int(550/0.8), int(300/0.8))
	cv2.imshow('main', cv2.cvtColor(np.array(segment), cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF==ord('q'):
		cv2.destroyAllWindows()
		sys.exit()


def show_screen_color():
	segment = np.array(ImageGrab.grab(bbox=(400, 400, 950, 700)))
	cv2.namedWindow("main", cv2.WINDOW_NORMAL)
	cv2.resizeWindow('main', int(550/0.8), int(300/0.8))
	cv2.imshow('main', cv2.cvtColor(np.array(segment), cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF==ord('q'):
		cv2.destroyAllWindows()
		sys.exit()


if __name__ == '__main__':
	while True:
		show_screen_color()
