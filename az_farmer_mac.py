from PIL import ImageGrab
import os
import time
import json
import datetime
from az_code_mac import *
from PIL import ImageOps
from numpy import *
import numpy as np
import timeit
import cv2
import warnings
import subprocess
from keyboard import *

boar_exist_int = [324, 325, 326, 497, 482, 490, 492, 496, 495, 498, 517, 662, 665, 494, 500, 419, 578, 623, 672, 693, 778, 805, 562, 838, 988, 1014, 1189, 1356, 1507, 1571, 5797, 6499]


def boar_exists(cords):
    """ return true if on mouse-over at cord a boar hover is observed"""
    x = cords[0]
    y = cords[1]
    box = (x*2, y*2-55, x*2+30, y*2-50 )
    left_box = (x*2-80, y*2, x*2-50, y*2+5 )
    mousePos((x,y))
    time.sleep(1)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    #im.save('test.png', dpi=(116,116))
    bm = ImageOps.grayscale(ImageGrab.grab(left_box))
    bm.save('left_test.png', dpi=(116,116))
    b = array(bm.getcolors())
    b = b.sum()
    print(a, b)
    for i in boar_exist_int:
    	if i in [a, b]:
    		print("OMG BOAR HERE, GET EM!")
    		return True
    return False


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


def spawner(file_name, location, hunt_type):
    """return a list of tuples given a sequence file
    [[(), (), (), ()], [(), (), (), ()]]
    """
    sequence = load_file(file_name)
    spawns = []
    loc = sequence['sequence']['loc']
    n = len(loc)-1
    while n >= 0:
        n -= 1
        if loc[n]['name'] == location:
            if hunt_type == 'fish':
                spawn_inc = loc[n][hunt_type][0]['spawns']
                spawn_len = len(spawn_inc)-1
                spawns = []
                while spawn_len >= 0:
                    spawns_temp = (spawn_inc[spawn_len]['x'], spawn_inc[spawn_len]['y'])
                    spawns.append(spawns_temp)
                    spawn_len -= 1
                return spawns
            elif hunt_type == 'boars':
                boar_spawns = []
                for i in range(len(loc[n][hunt_type])):
                    data = loc[n][hunt_type][i]['spawns']
                    data_len = len(data)-1
                    spawns = []
                    while data_len >= 0:
                        spawns_temp = (data[data_len]['x'], data[data_len]['y'])
                        spawns.append(spawns_temp)
                        data_len -= 1
                    boar_spawns.append(spawns)
                return boar_spawns


def get_start_point(file_name, location, hunt_type, ind):
    sequence = load_file(file_name)
    nav_list = sequence['sequence']['loc']
    for i in nav_list:
        if i['name'] == location:
            ret_loc = (i[hunt_type][ind]['start_point']['x'], i[hunt_type][ind]['start_point']['y'])
            return ret_loc


def farmer(file_name, location, hunt_type, timer=2.5):
    time.sleep(2)
    cord_list = spawner(file_name, location, hunt_type)
    navy(location)
    time.sleep(2)
    if hunt_type == 'fish':
        print("{} : Fishing started @ {}".format(datetime.datetime.now(),location))
        move_and_click(get_start_point(file_name, location, hunt_type, 0),5)
        for i in cord_list:
            if boar_exists(i):
                move_and_click(i, timer)
            else:
                print("Move along, no fish here... continuing to next cord")
    else:
        print("Gimme dem Boars!")
        #time.sleep(2)
        if type(cord_list[0]) != list:
            n = 3
            while n > 0:
                print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
                move_and_click(get_start_point(file_name, location, hunt_type, 0),5)
                for i in cord_list:
                    if boar_exists(i):
                        move_and_click(i, timer)
                    else:
                        print("Move along, no boar here... continuing to next cord")
                n -= 1
        else:
            for i in range(len(cord_list)):
                n = 3
                while n > 0:
                    print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
                    move_and_click(get_start_point(file_name, location, hunt_type, i),5)
                    for x in cord_list[i]:
                        if boar_exists(x):
                            move_and_click(x, timer)
                        else:
                            print("Move along, no boar here... continuing to next cord")
                    n -= 1

    
def does_boar_exist_cursor():
    mouse.click(Button.left, 1)
    data = output_cords()
    cord = (data['x'], data['y'])
    boar_exists(cord)


def segment_grab(x, y, w, l, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("segment.png", 'PNG')
        params = ['mogrify', 'segment.png', 'segment.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im

def cursor_grab(tag=''):
    x, y = mouse.position
    width = 20
    length = 20
    box = (x*2-width, y*2-length, x*2+width, y*2+length)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    im.save("Cursor_at_{}-{}-{}.png".format(x, y, tag), 'PNG')


trs_x = 400*2
trs_y = 200*2
trs_w = 1200*2
trs_h = 1000*2
method = cv2.TM_CCOEFF_NORMED
threshold = 0.90

boar_templates = [  'boar_static.png',
                    'boar_down.png', 
                    'boar_partial_1.png', 
                    'boar_partial_2.png',
                    'boar_partial_3.png',
                    'boar_1.png', 
                    'boar_2.png', 
                    'boar_3.png', 
                    'boar_4.png',
                    'b1.png',
                    'b2.png',
                    'b3.png',
                    'b4.png',
                    'b5.png',
                    'b6.png',
                    'b7.png',
                    'b8.png',
                    'b9.png',
                    'b10.png'
                ]

boar_templates_loaded = []
for boar_tmp in boar_templates:
    boar_tmp = cv2.imread(boar_tmp, cv2.IMREAD_GRAYSCALE)
    boar_templates_loaded.append(boar_tmp)

def get_boar_locs(template_list):
    """Given a segment, clear the segment by clicking an element from the list of templates"""
    loc_list = []
    segment_grab(trs_x, trs_y, trs_w, trs_h)
    for temp in template_list:
        template = cv2.imread(temp, cv2.IMREAD_GRAYSCALE)
        full_image = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(full_image, template, method)
        loc = np.where(result>=threshold)
        print(loc)
        mn, mx, mnLoc, mxLoc = cv2.minMaxLoc(result)
        MPx, MPy = mxLoc
        for pos in zip(*loc[::-1]):
            print(temp)
            loc_list.append((MPx, MPy))
    data = (list(dict.fromkeys(loc_list)))
    #print(data)
    return data


def clear_segment(template_list):
    """ Given a segment and a list of boar locations, click the locations """
    locs = get_boar_locs(template_list)
    while len(locs) > 0:
        for loc in locs:
            go_to_boar(loc, 10)
            break
        locs = get_boar_locs(template_list)


def go_to_boar(loc, timer):
    x = (trs_x/2+loc[0]/2)+5
    y = (trs_y/2+loc[1]/2)+5
    mousePos((x, y))
    time.sleep(0.2)
    mousePos((x, y))
    mouse.click(Button.left, 2)
    time.sleep(timer)


def mouse_to_boar(loc):
    x = trs_x/2+loc[0]/2
    y = trs_y/2+loc[1]/2
    mousePos((x, y))
    print(x, y)


def find_image_in_segment(img, trs_x, trs_y, trs_w, trs_h):
    seg = segment_grab(trs_x, trs_y, trs_w, trs_h,False)
    template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)


def clear_segment_type_2(template_list):
    segment_grab(trs_x, trs_y, trs_w, trs_h)
    for temp in template_list:
        segment_grab(trs_x, trs_y, trs_w, trs_h)
        go_to_first_found(temp)


def go_to_first_found(img):
    segment = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    if len(fres) <= 0:
        print("no match... continuing")
        return
    else:
        for i in (zip(*fres[::-1])):
            x, y = i
            print("boar found at {} {} using {}".format(x, y, img))
            go_to_boar(i, 5)
            break


def draw_cord(img):
    segment_grab(trs_x, trs_y, trs_w, trs_h)
    segment = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, template, method)
    fres = np.where(result >= threshold)
    w, h = template.shape
    for i in (zip(*fres[::-1])):
        cords = (i[0]+w, i[1]+h)
        cv2.circle(segment, (cords), 15, (0,0,255), -1)
        print((i[0]+w, i[1]+h))
    cv2.imwrite('result-{}.png'.format(img), segment)


def write_cords_optimised(img):
    c_list = []
    segment = cv2.imread('segment.png', cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(segment, img, method)
    fres = np.where(result >= threshold)
    x_b = 100
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


def remove_bounded_entries(cord_list, b_x, b_y):
    out_list = []
    #print("DEBUG: RDE: outlist pre-check: {}".format(out_list))
    cord_list = sort_list(cord_list)
    for cord in cord_list:
        if len(out_list) == 0:
            prv_x = 0
            prv_y = 0
        x, y = cord
        if x > prv_x+b_x or x < prv_x-b_x or y > prv_y+b_y or y < prv_y-b_y:
            out_list.append(cord)
            prv_x, prv_y = cord
    #print("Out_list: {}".format(out_list))
    return out_list


def write_cords_to_file(img, cord_list, n):
    segment = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    for cord in cord_list:
        cv2.circle(segment, (cord[0], cord[1]), 15, (0,0,255), -1)
    cv2.imwrite('final-{}.png'.format(n), segment)


def sort_list(unsorted_list):
    unsorted_list.sort(key=lambda tup: tup[1])
    return unsorted_list


def clear_segment_type_3(n):
    data = combined_cords(boar_templates_loaded)
    c_l = remove_bounded_entries(data, 100, 40)
    write_cords_to_file('segment.png', c_l, n)
    for c in c_l:
        print("Going to boar @: {}".format(c))
        time.sleep(1)
        go_to_boar(c, 10)
    data = []
    c_l = []
    #print(c_l)


def cycle():
    n = 4
    navy('bottom_right', 6)
    move_and_click((1233, 737), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    navy('bottom_left', 6)
    move_and_click((880, 662), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    navy('top_right', 6)
    move_and_click((1259, 662), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    fish_path()


def fish_path():
    print("Starting Fishing now!")
    navy('top_right', 6)
    time.sleep(1)
    move_and_click((806, 398), 20) # Start
    time.sleep(1)
    move_and_click((1054, 300), 5) # Point TR1
    move_and_click((692, 312), 5)
    navy('top_left', 6)
    time.sleep(1)
    move_and_click((962, 897), 20) # Start
    move_and_click((797, 387), 5)
    move_and_click((1093, 413), 5)
    move_and_click((1056, 846), 5)
    move_and_click((1164, 1107), 5)
    move_and_click((1487, 639), 15) #SP
    move_and_click((1284, 883), 5)
    move_and_click((1336, 597), 5)
    move_and_click((1419, 333), 5)
    navy('top_left', 6)
    time.sleep(1)
    move_screen_right(2, 350)
    time.sleep(1)
    navy('top_left', 6)
    time.sleep(1)
    move_screen_right(2, 350)
    time.sleep(1)
    move_and_click((950, 351), 3)
    move_and_click((1217, 310), 3)
    move_and_click((1443, 320), 3)
    navy('top_left', 6)
    time.sleep(1)
    move_screen_right(2, 350)
    time.sleep(1)
    navy('top_left', 6)
    time.sleep(1)
    move_screen_right(2, 350)
    time.sleep(1)
    move_screen_down(1, 300)
    time.sleep(1)
    move_and_click((1165, 767), 10)
    move_and_click((1106, 897), 5)
    move_and_click((1045, 1073), 5)


def multi_window_run():
    while True:
        print("Running Cycle")
        cycle()
        print("Swapping Windows")
        swap_windows()
        time.sleep(3)


if __name__ == '__main__':
    #fish_path()
    multi_window_run()
    #cord_list = []
    #output_cords()
    #cursor_grab_iter(4, 3)
    