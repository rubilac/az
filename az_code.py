from PIL import ImageGrab
import os
import time
import win32api, win32con
import json
import datetime

#Globals
#x_pad = 979
#y_pad = 356

x_pad = 0
y_pad = 0

def screenGrab():
    box = (x_pad+1, y_pad+1, x_pad+640, y_pad+479)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')


def get_location(file_name):
	load_file(file_name)


def leftClick(cords):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print "Left click @ {}".format(cords)


def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    #print 'left Down'


def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    #print 'left release'


def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))


def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x,y

def output_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    build_output = {"x": x,"y": y}
    #print x,y
    print build_output
    return build_output


def move_and_click(pos, sleep_time=3):
    mousePos(pos)
    leftClick(pos)
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
        move_screen((700, 217), (717-dist, 217))
        num_times -= 1


def move_screen_down(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((442, 662), (442, 662-dist))
        num_times -= 1    


def move_screen_left(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((0, 217), (0+dist, 217))
        num_times -= 1


def move_screen_up(num_times=1, dist=100):
    """ input: num_times - the number of times to move
                dist - how far to move
    """
    while num_times > 0:
        move_screen((442, 662), (442, 662+dist))
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

def nav_bot_r(num_moves):
    move_screen_right(num_moves, 700)
    move_screen_down(num_moves,200)


def nav_top_r(num_moves):
    move_screen_right(num_moves, 700)
    move_screen_up(num_moves, 200)


def nav_top_l(num_moves):
    move_screen_up(num_moves, 200)
    move_screen_left(num_moves, 700)


def nav_bot_l(num_moves):
    move_screen_down(num_moves,200)
    move_screen_left(num_moves, 700)


def load_file(file_name):
    with open(file_name) as f:
        data=json.load(f)
    return data


def create_tuple():
    pass


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


if __name__ == '__main__':
   	output_cords()