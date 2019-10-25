import pyscreenshot as ImageGrab
import os
from az_code import *
from az_farmer import *
from PIL import Image
from PIL import ImageOps
from numpy import *
from pytesseract import image_to_string
import pytesseract
from tesserocr import PyTessBaseAPI

# 1916 x 927
trs_x = 998
trs_y = 150
trs_w = 1013
trs_h = 165

food_cords = (980, 150, 1015, 165)


images = ['10,979.jpg', '17slash34.jpg', '2,255.jpg', '400.jpg', '67.jpg']
images_bw = ['10,979_bw.jpg', '17slash34_bw.jpg', '2,255_bw.jpg', '400_bw.jpg', '67_bw.jpg']
# ,


def fixup_images():
	for image in images:
		column = Image.open(image)
		gray = column.convert('L')
		blackwhite = gray.point(lambda x: 0 if x < 140 else 255, '1')
		name = image.split('.')
		new_name = "{}_bw.jpg".format(name[0])
		blackwhite.save(new_name)


def fixup_image(image):
	column = Image.open(image)
	gray = column.convert('L')
	blackwhite = gray.point(lambda x: 0 if x < 145 else 255, '1')
	blackwhite.save(image)


def get_num_from_image(image):
	#fixup_image(image)
	api = PyTessBaseAPI(path='/opt/dev/az/tessdata/.', lang='eng', psm=7, oem=3)
	api.SetVariable('tessedit_char_whitelist', '/0123456789')
	api.SetImageFile(image)
	#print(api.GetUTF8Text())
	return api.GetUTF8Text()


if __name__ == '__main__':
	#segment_grab_custom(food_cords, 'food')
	get_num_from_image('segment_food.jpg')
	#fixup_images()
	#print("Colour Images")
	#for image in images:
	#	get_num_from_image(image)
	#print(ocr_core('out.png'))
	#print(ocr_core('segment_total.png'))