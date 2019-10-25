from PIL import Image
import os
import time
#import win32api, win32con
import json
import datetime
from pynput.mouse import Button, Controller 
import pynput.mouse
from PIL import ImageOps
#from az_crafting import *
#from az_farmer_mac import *

mouse = pynput.mouse.Controller()

x_pad = 0
y_pad = 0

def screenGrab(tag='default'):
    box = (x_pad+1, y_pad+1, x_pad+2400, y_pad+2400)
    imgray = ImageOps.grayscale(ImageGrab.grab(box))
    imcol = ImageGrab.grab(box)
    imcol.save('{}_color.png'.format(tag), 'PNG')
    imgray.save('{}_gray.png'.format(tag), 'PNG')


def get_location(file_name):
	load_file(file_name)


def leftClick(cords):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print "Left click @ {}".format(cords)


def leftDown():
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    mouse.press(Button.left)
    time.sleep(.1)
    #print 'left Down'


def leftUp():
    #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    mouse.release(Button.left)
    time.sleep(.1)
    #print 'left release'


def mousePos(cord):
    #win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
    mouse.position = (cord[0], cord[1])

def get_cords():
    x, y = mouse.position()
    #x,y = win32api.GetCursorPos()
    print(x,y)

def output_cords():
    #x,y = win32api.GetCursorPos()
    x, y = mouse.position
    build_output = {"x": int(x),"y": int(y)}
    print(int(x),int(y)) 
    print(build_output)
    return build_output


def move_and_click(pos, sleep_time=3):
    mousePos(pos)
    mouse.click(Button.left, 1)
    time.sleep(sleep_time)


def move_screen(start_point, end_point):
    """input:
        start_point
        end_point
        Use start_point and leftdown and move mouse to endpoint
    """
    mousePos(start_point)
    time.sleep(0.1)
    leftDown()
    mousePos(end_point)
    time.sleep(0.1)
    leftUp()


def move_screen_right(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((500, 600), (500-dist, 600))
        num_times -= 1


def move_screen_down(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((480, 600), (480, 600-dist))
        num_times -= 1    


def move_screen_left(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((500, 600), (500+dist, 600))
        num_times -= 1


def move_screen_up(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((500, 600), (500, 600+dist))
        num_times -= 1


def navy(nav_indicator, num_moves=4):
    if nav_indicator == "top_right":
        nav_top_r(num_moves)
    elif nav_indicator == "bottom_right":
        nav_bot_r(num_moves)
    elif nav_indicator == "bottom_left":
        nav_bot_l(num_moves)
    elif nav_indicator == "top_left":
        nav_top_l(num_moves)


def nav_to_town():
    move_screen_right(5, 400)
    move_screen_up(4, 200)
    move_screen_left(1, 400)


def nav_bot_r(num_moves):
    move_screen_right(num_moves, 400)
    move_screen_down(num_moves,200)


def nav_top_r(num_moves):
    move_screen_right(num_moves, 400)
    move_screen_up(num_moves, 200)


def nav_top_l(num_moves):
    move_screen_up(num_moves, 200)
    move_screen_left(num_moves, 400)


def nav_bot_l(num_moves):
    move_screen_down(num_moves,200)
    move_screen_left(num_moves, 400)


def load_file(file_name):
    with open(file_name) as f:
        data=json.load(f)
    return data


def create_tuple():
    pass

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


def execute_sequence(file_name):
    sequence = load_file(file_name)
    nav_list = []
    for i in sequence['loc']:
        nav_list.append()


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
            move_and_click(i,timer)
    else:
        print("Gimme dem Boars!")
        time.sleep(2)
        if type(cord_list[0]) != list:
            n = 3
            while n > 0:
                print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
                move_and_click(get_start_point(file_name, location, hunt_type, 0),5)
                for i in cord_list:
                    move_and_click(i, timer)
                n -= 1
        else:
            for i in range(len(cord_list)):
                n = 3
                while n > 0:
                    print("{} : Boar Round: {} started @ {}".format(datetime.datetime.now(), n, location))
                    move_and_click(get_start_point(file_name, location, hunt_type, i),5)
                    for x in cord_list[i]:
                        move_and_click(x, timer)
                    n -= 1

    
def world_tour_2560(file_name):
	time.sleep(2)
	navy('bottom_right')
	move_and_click(get_start_point(file_name, 'bottom_right', 'boars', 0),15)
	farmer(file_name, 'bottom_right', 'boars', 2)
	farmer(file_name, 'bottom_right', 'fish', 10)
	navy('bottom_left')
	move_and_click(get_start_point(file_name, 'bottom_left', 'boars', 0),15)
	farmer(file_name, 'bottom_left', 'boars', 2)
	farmer(file_name, 'bottom_left', 'fish', 10)


def world_tour_1920(file_name):
    time.sleep(2)
    #navy('bottom_right')
    move_and_click(get_start_point(file_name, 'bottom_right', 'boars', 0), 3)
    farmer(file_name, 'bottom_right', 'boars', 3)
    farmer(file_name, 'bottom_right', 'fish', 10)



def get_test_images():
    navy('top_right', 4)
    screenGrab("test_bt_tr")
    navy('bottom_right', 4)
    screenGrab("test_bt_br")
    navy('bottom_left', 4)
    screenGrab("test_bt_bl")
    navy("top_left", 4)
    screenGrab("test_bt_tr")


if __name__ == '__main__':
    mousePos()
    #get_cords()
    #screenGrab()
    #get_test_images()
