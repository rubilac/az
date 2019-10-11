import pyscreenshot as ImageGrab
import os
import time
import json
import datetime
from az_code import *
from az_crafting import *
from PIL import ImageOps
from numpy import *
import numpy as np
import timeit
import cv2
import warnings
import subprocess
from keyboard import *


trs_x = 70
trs_y = 140
trs_w = 1256
trs_h = 920
method = cv2.TM_CCOEFF_NORMED
threshold = 0.8
refresh_button = (667, 589)
refresh_img = '/opt/dev/az/templates/refresh.png'

template_path_boar = '/opt/dev/az/templates/boar/'
load_boars = os.listdir(template_path_boar)
boar_templates_loaded = []
for boar_tmp in load_boars:
    boar_tmp = cv2.imread(template_path_boar+boar_tmp, cv2.IMREAD_GRAYSCALE)
    boar_templates_loaded.append(boar_tmp)


def get_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)


def refresh_checker(pp=''):
    template = cv2.imread(refresh_img)
    refresh_grab()
    screen = cv2.imread('tmp_refresh.png')
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= 0.99)
    try:
        test = fres[0][0]>0
        #print(fres)
        print("Refresh Button Found. Waiting 5s before clicking...")
        time.sleep(5)
        move_and_click(refresh_button)
        print("Clicked Refresh, waiting 20s for before continuing")
        time.sleep(15)
        if pp == '':
            return
        else:
            navy(pp)
    except:
        #print("No refresh button found")
        pass


def get_image_info(img):
    """Given an image, return the dtype and shape"""
    template = cv2.imread(img)
    print("DType: {}".format(template.dtype))
    print("Shape: {}".format(template.shape))


def cursor_grab_iter(num, timer):
    while num > 0:
        cursor_grab(num)
        num -= 1
        time.sleep(timer)

  
def refresh_grab(x=500, y=500, w=800, l=700, save=True):
    new_cord = (x, y, w, l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("tmp_refresh.png", 'PNG')
        params = ['mogrify', 'tmp_refresh.png', 'tmp_refresh.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def segment_grab(x, y, w, l, save=True):
    new_cord = (x, y, w, l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("segment.png", 'PNG')
        params = ['mogrify', 'segment.png', 'segment.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def named_segment_grab(x, y, w, l, name, save=True):
    new_cord = (x, y, w, l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("segment_{}.png".format(name), 'PNG')
        params = ['mogrify', 'segment.png', 'segment.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def town_grab(x, y, w, l, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("town.png", 'PNG')
        params = ['mogrify', 'town.png', 'town.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def popup_grab(x, y, w, l, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("popup.png", 'PNG')
        params = ['mogrify', 'popup.png', 'popup.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def cursor_grab(tag=''):
    x, y = mouse.position
    width = 15
    length = 15
    box = (x*2-width, y*2-length, x*2+width, y*2+length)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    im.save("Cursor_at_{}-{}-{}.png".format(x, y, tag), 'PNG')


def cursor_grab_color(width, length, tag=''):
    x, y = mouse.position
    box = (x*2-width, y*2-length, x*2+width, y*2+length)
    im = ImageGrab.grab(box)
    im.save("Cursor_at_{}-{}-{}.png".format(x, y, tag), 'PNG')
    imarr = np.array(im)
    print(np.array(imarr).sum())
    print(int(x), int(y))
    

def cursor_grab_iter_color(num, timer, w, h):
    while num > 0:
        cursor_grab(w, h, num)
        num -= 1
        time.sleep(timer)


def cursor_grab_iter_color(num, timer, w, h):
    while num > 0:
        cursor_grab_color(w, h, num)
        num -= 1
        time.sleep(timer)


def go_to_boar(loc, timer):
    x = (trs_x+loc[0])+5
    y = (trs_y+loc[1])+5
    mousePos((x, y))
    time.sleep(0.2)
    mousePos((x, y))
    mouse.click(Button.left, 1)
    time.sleep(timer)


def draw_cord(img, trs_x=trs_x, trs_y=trs_y, trs_w=trs_w, trs_h=trs_h):
    segment_grab(trs_x, trs_y, trs_w, trs_h)
    segment = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    w, h = template.shape
    for i in (zip(*fres[::-1])):
        cords = (i[0]+w, i[1]+h)
        cv2.circle(segment, (cords), 35, (0,0,255), -1)
        print((i[0]+w, i[1]+h))
    cv2.imwrite('result-{}.png'.format(img), segment)


def write_draw_cord(img, trs_x=trs_x, trs_y=trs_y, trs_w=trs_w, trs_h=trs_h):
    named_segment_grab(trs_x, trs_y, trs_w, trs_h, n)
    segment = cv2.imread('segment_{}.png'.format(n), cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    w, h = template.shape
    for i in (zip(*fres[::-1])):
        cords = (i[0]+w, i[1]+h)
        cv2.circle(segment, (cords), 35, (0,0,255), -1)
        print((i[0]+w, i[1]+h))
    cv2.imwrite('result-{}.png'.format(img), segment)


def write_cords_optimised(img):
    c_list = []
    segment = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, img, method)
    fres = np.where(result >= threshold)
    x_b = 80
    y_b = 20
    prv_x = 0
    prv_y = 0
    for i in (zip(*fres[::-1])):
        x = i[0]
        y = i[1]
        if x > prv_x+x_b or x < prv_x-x_b or y > prv_y+y_b or y < prv_y-y_b:
            c_list.append(i)
            cv2.circle(segment, (x, y), 15, (0,0,255), -1)
            prv_x = i[0]
            prv_y = i[1]
    cv2.imwrite('result-optimised.png'.format(img), segment)
    return c_list


def combined_cords(template_list):
    segment_grab(trs_x, trs_y, trs_w, trs_h)
    cord_list = []
    c_list = []
    for img in template_list:
        data = write_cords_optimised(img)
        for i in data:
            cord_list.append(i)
    return cord_list


def write_combined_cords(template_list, n):
    named_segment_grab(trs_x, trs_y, trs_w, trs_h, n)
    cord_list = []
    c_list = []
    for img in template_list:
        data = write_cords_optimised(img)
        for i in data:
            cord_list.append(i)
    return cord_list

def remove_bounded_entries(cord_list, b_x, b_y):
    out_list = []
    cord_list = sort_list(cord_list)
    for cord in cord_list:
        if len(out_list) == 0:
            prv_x = 0
            prv_y = 0
        x, y = cord
        if x > prv_x+b_x or x < prv_x-b_x or y > prv_y+b_y or y < prv_y-b_y:
            out_list.append(cord)
            prv_x, prv_y = cord
    return out_list


def write_cords_to_file(img, cord_list, n):
    segment = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    for cord in cord_list:
        cv2.circle(segment, (cord[0], cord[1]), 15, (0,0,255), -1)
    cv2.imwrite('final-{}.png'.format(n), segment)


def sort_list(unsorted_list):
    unsorted_list.sort(key=lambda tup: tup[1])
    return unsorted_list


def clear_segment_type(n):
    refresh_checker()
    data = combined_cords(boar_templates_loaded)
    c_l = remove_bounded_entries(data, 100, 40)
    write_cords_to_file('segment.png', c_l, n)
    for c in c_l:
        print("Going to boar @: {}".format(c))
        time.sleep(1)
        go_to_boar(c, 10)
    data = []
    c_l = []


def write_segment(n):
    refresh_checker()
    data = write_combined_cords(boar_templates_loaded, n)
    c_l = remove_bounded_entries(data, 100, 40)
    write_cords_to_file('segment_{}.png'.format(n), c_l, n)
    data = []
    c_l = []


def get_anchor():
    """ Get the cords of the anchor """
    threshold = 0.99
    segment = cv2.imread("segment.png", cv2.IMREAD_GRAYSCALE)
    try:
        template = cv2.imread("/opt/dev/az/templates/anchor_2.png", cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(segment, template, method)
        fres = np.where(result >= threshold)
        cord = (int(fres[1]), int(fres[0]))
        print("Anchor Found @ : {}".format(cord))
        return cord
    except:
        template = cv2.imread("/opt/dev/az/templates/popup_anchor.png", cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(segment, template, method)
        fres = np.where(result >= threshold)
        cord = (int(fres[1]/2), int(fres[0]/2))
        print("Popup Anchor Found @ : {}".format(cord))
        return cord        


def is_ready():
    """ Check if a building is working """
    threshold = 0.90
    segment = cv2.imread("town.png", cv2.IMREAD_GRAYSCALE)
    template = cv2.imread("/opt/dev/az/templates/ready_2.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    try:
        type(fres[0][0])
        return 0 # working
    except IndexError:
        return 1 # ready for work


def ready_custom(full_path):
    """ Check if a building is working """
    threshold = 0.99
    segment = cv2.imread("town.png", cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    try:
        type(fres[0][0])
        return 0 # working
    except IndexError:
        return 1 # ready for work    


def is_popup():
    """ Check if a popup exists """
    threshold = 0.99
    segment = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    template = cv2.imread("/opt/dev/az/templates/close.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    try:
        type(fres[0][0])
        cord = (int(fres[1]/2), int(fres[0]/2))
        print("Popup found @ : {}".format(cord))
        return cord
    except IndexError:
        return 1 # ready for work   


def cycle():
    move_and_click((688, 123)) #Focus Frame
    n = 4
    refresh_checker()
    navy('bottom_right', 6)
    time.sleep(2)
    move_and_click((802, 404), 10) # Starting Position for bottom right boar farm
    time.sleep(0.2)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('top_left', 6)
    time.sleep(2)
    move_and_click((451, 395), 4)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('bottom_left', 6)
    time.sleep(2)
    move_and_click((762, 978), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('top_right', 6)
    time.sleep(2)
    move_and_click((935, 702), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    fish_path()


def one_cycle():
    refresh_checker()
    move_and_click((688, 123)) #Focus Frame
    navy('bottom_right', 6)
    time.sleep(1)
    move_and_click((802, 404), 10) # Starting Position for bottom right boar farm
    time.sleep(0.2)
    clear_segment_type(1)


def get_anchored_cursor(anchor):
    #anchor = get_anchor()
    global_cord = output_cords()
    dx = anchor[0] - global_cord['x']
    dy = anchor[1] - global_cord['y']
    out_cords = (-dx, -dy)
    print(out_cords)


def fish_path():
    segment_grab(trs_x, trs_y, trs_w, trs_h, True)
    anchor = get_anchor()
    print("Starting Fishing now!")
    refresh_checker()
    navy('top_left', 6)
    mousePos(anchor_convert(anchor,(-666, 336)))
    move_and_click(anchor_convert(anchor,(-666, 336)), 20) #Top left Start
    mousePos(anchor_convert(anchor, (-745, 286)))
    move_and_click(anchor_convert(anchor, (-745, 286)), 5)
    mousePos(anchor_convert(anchor, (-517, 309)))
    move_and_click(anchor_convert(anchor, (-517, 309)), 5)
    mousePos(anchor_convert(anchor, (-531, 656)))
    move_and_click(anchor_convert(anchor, (-531, 656)), 5)
    mousePos(anchor_convert(anchor, (-451, 863)))
    move_and_click(anchor_convert(anchor, (-451, 863)), 5)
    refresh_checker()
    navy('bottom_left', 6)
    mousePos(anchor_convert(anchor, (-27, 736)))
    move_and_click(anchor_convert(anchor,(-27, 736)), 15) # Middle Bottom Start
    mousePos(anchor_convert(anchor, (14, 721)))
    move_and_click(anchor_convert(anchor, (14, 721)), 5) # Bridge fish
    mousePos(anchor_convert(anchor, (55, 577)))
    move_and_click(anchor_convert(anchor, (55, 577)), 5) # Probably wrong
    mousePos(anchor_convert(anchor, (-356, 334)))
    move_and_click(anchor_convert(anchor, (-356, 334)), 8)
    refresh_checker()
    navy('bottom_left', 6)
    move_screen_up(4, 300)
    mousePos(anchor_convert(anchor, (-202, 530)))
    move_and_click(anchor_convert(anchor,(-202, 530)), 15) #Middle Top Start
    mousePos(anchor_convert(anchor, (-310, 459)))
    move_and_click(anchor_convert(anchor, (-310, 459)), 5)
    mousePos(anchor_convert(anchor, (-244, 244)))
    move_and_click(anchor_convert(anchor, (-244, 244)), 5)
    mousePos(anchor_convert(anchor, (-59, 260)))
    move_and_click(anchor_convert(anchor, (-59, 260)), 5)
    refresh_checker()
    navy('top_right', 6)
    time.sleep(2)
    mousePos(anchor_convert(anchor, (-702, 279)))
    move_and_click(anchor_convert(anchor, (-702, 279)), 5) #Top right Start 
    mousePos(anchor_convert(anchor, (-786, 227)))
    move_and_click(anchor_convert(anchor,(-786, 227)), 15)    
    mousePos(anchor_convert(anchor, (-600, 228)))
    move_and_click(anchor_convert(anchor, (-600, 228)), 5)
    mousePos(anchor_convert(anchor, (-314, 217)))
    move_and_click(anchor_convert(anchor, (-314, 217)), 5)


def secure_click(cord, anchor='', delay=0.2):
    if anchor == '':
        cord = cord
    else:
        cord = anchor_convert(anchor, cord)
    mousePos(cord)
    time.sleep(0.1)
    mousePos(cord)
    time.sleep(0.1)
    move_and_click(cord, delay)


def secure_mouse_over(cord, anchor='', delay=0.2):
    if anchor == '':
        cord = cord
    else:
        cord = anchor_convert(anchor, cord)
    print(cord)
    mousePos(cord)
    time.sleep(0.1)
    mousePos(cord)
    time.sleep(0.1)


def is_limit_reached(anchor):
    threshold = 0.95
    segment_grab(trs_x, trs_y, trs_w, trs_h, True)
    segment = cv2.imread('segment.png',  cv2.IMREAD_GRAYSCALE)
    template = cv2.imread('limit_reached.png', cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    if len(fres[0]) >= 1:
        secure_click((-351, 296), anchor)


def collect_path():
    segment_grab(trs_x, trs_y, trs_w, trs_h, True)
    anchor = get_anchor()
    print("Starting Collecting now!")
    navy('top_right', 4)
    secure_click((15, 162), anchor, 1)
    secure_click((-1025, 634), anchor, 1)
    secure_click((-942, 543), anchor, 1)
    secure_click((-832, 595), anchor, 1)
    navy('bottom_right', 2)
    secure_click((-178, 694), anchor, 1)
    move_screen_left(2, 300)
    secure_click((-592, 860), anchor, 1)
    secure_click((-178, 694), anchor, 1)
    navy('bottom_left', 2)
    secure_click((-814, 815), anchor, 1)
    navy('top_left', 3)
    secure_click((-830, 468), anchor, 1)
    secure_click((-530, 294), anchor, 1)


def anchor_convert(anchor, cord):
    return (anchor[0]+cord[0], anchor[1]+cord[1])


def write_cycle(n, x):
    refresh_checker()
    move_and_click((688, 123)) #Focus Frame
    navy('bottom_right', 6)
    time.sleep(1)
    move_and_click((802, 404), 10) # Starting Position for bottom right boar farm
    time.sleep(0.2)
    write_segment(1, x)


def write_boars_to_segment_n(n):
    while n > 0:
        write_segment(n)
        time.sleep(0.5)
        n -= 1


def multi_window_run():
    print("Running Cycle")
    cycle()
    time.sleep(3)
    print('Collecting RP!')

if __name__ == '__main__':
    #segment_grab(trs_x, trs_y, trs_w, trs_h)
    multi_window_run()
    #fish_path()
    #anchor = get_anchor()
    #get_anchored_cursor(anchor)
    #collect_path()
    #cycle()
    #refresh_checker()