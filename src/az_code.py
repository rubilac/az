import pyscreenshot as ImageGrab
import os
import time
import json
import datetime
from pynput.mouse import Button, Controller 
import pynput.mouse
from PIL import ImageOps

mouse = pynput.mouse.Controller()

x_pad = 70
y_pad = 140
res_w = 1256
res_h = 920


def screenGrab(tag='default'):
    box = (x_pad, y_pad, res_w, res_h)
    imgray = ImageOps.grayscale(ImageGrab.grab(box))
    imcol = ImageGrab.grab(box)
    imcol.save('{}_color.png'.format(tag), 'PNG')
    imgray.save('{}_gray.png'.format(tag), 'PNG')


def get_location(file_name):
    #asd
    load_file(file_name)


def leftDown():
    #asd
    mouse.press(Button.left)
    time.sleep(.1)


def leftUp():
    mouse.release(Button.left)
    time.sleep(.1)


def mousePos(cord, n=0):
    #asd
    mouse.position = (cord[0], cord[1])
    time.sleep(n)


def get_cords():
    x, y = mouse.position
    print((x,y))
    return x, y


def get_relative_cords():
    x,y = get_cords()
    if x_pad + x > res_w or y_pad + y > res_h:
        print("Cord out of range!")
        return False
    print("Relative Coordinate: {}, {}".format(x_pad + x, y_pad + y))
    return(x_pad + x,  y_pad + y)


def output_cords():
    #x,y = win32api.GetCursorPos()
    x, y = mouse.position
    build_output = {"x": int(x),"y": int(y)}
    print(int(x),int(y)) 
    print(build_output)
    return build_output


def move_and_click(pos, sleep_time=1):
    mousePos(pos, 1)
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
    move_screen_left(1, 200)


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
    #mousePos((569, 527))
    #move_and_click((688, 123)) # Focus Chrome frame!
    #screenGrab()
    get_cords()
    #get_test_images()
    #nav_to_town()