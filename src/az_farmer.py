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
trs_y = 100
trs_w = 1470
trs_h = 927
method = cv2.TM_CCOEFF_NORMED
threshold = 0.8

# Anchor = (1324, 46)

# Button positions
refresh_button = (769, 571)# (666, 590)
decline_special_offer = (-421, 598)#
ok_pos = (826, 684) # (720, 703)  #
complete_pos = (711, 681) # (638, 702) #
sesterce_close_pos = (1040, 392) #
roman_helmets_close_pos = (1039, 361)# (936, 378)#
legion_approaching_pos = (894, 387)#
legion_defeat_pos = (595, 676)#
achievements_pos = (1064, 326)

# Image locations
refresh_img = '/opt/dev/az/templates/popups/refresh.png'
special_offer_img = '/opt/dev/az/templates/popups/special_offer.png'
ok_img = '/opt/dev/az/templates/popups/ok.png'
complete_img = '/opt/dev/az/templates/popups/complete.png'
sesterce_img = '/opt/dev/az/templates/popups/sesterce.png'
roman_helmets_img = '/opt/dev/az/templates/popups/roman_helmets.png'
legion_approaching_img = '/opt/dev/az/templates/popups/legion_approaching.png'
legion_defeat_img = '/opt/dev/az/templates/popups/legion_defeat.png'
achievements_img = '/opt/dev/az/templates/popups/achievements.png'


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


def refresh_checker():
    popup_grab()
    screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    threshold = 0.97
    popup_exists = False
    refresh_check()
    #special_offer_check(screen)
    ok_check(screen)
    quest_complete_check(screen)
    get_more_sesterce_check(screen)
    get_more_roman_helmets_check(screen)
    legion_approaching_check(screen)
    legion_defeated_check(screen)
    achievement_check(screen)

def refresh_check():
    template = cv2.imread(refresh_img)
    refresh_grab()
    screen = cv2.imread('tmp_refresh.png')
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= 0.80)
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


def special_offer_check(screen):
    template = cv2.imread(special_offer_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Special offer popup found, clicking decline!")
        secure_click(decline_special_offer, anchor, 1)
        time.sleep(1)
        secure_click((-417, 543), anchor, 1) #change
    except:
        pass


def ok_check(screen):
    template = cv2.imread(ok_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Ok button found, clicking ok!")
        secure_click(ok_pos, anchor, 1)
        time.sleep(1)
    except:
        pass


def quest_complete_check(screen):
    template = cv2.imread(complete_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Complete Quest popup found, clicking complete!")
        secure_click(complete_pos, anchor, 1)
        secure_click((769, 653), anchor, 1)
        print("Clicking OK")
        secure_click(ok_pos, anchor, 1)
        time.sleep(1)
    except:
        pass


def get_more_sesterce_check(screen):
    template = cv2.imread(sesterce_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Sesterce popup found, clicking X!")
        secure_click(sesterce_close_pos, anchor, 1)
        time.sleep(1)
        print("Clicking OK")
        #secure_click(sester)
    except:
        pass


def get_more_roman_helmets_check(screen):
    template = cv2.imread(roman_helmets_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Roman helmets popup found, clicking X!")
        secure_click(roman_helmets_close_pos, anchor, 1)
        time.sleep(1)
        print("Doing a cautionary sesterce check")
        popup_grab()
        screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
        get_more_sesterce_check(screen)
    except:
        pass


def legion_approaching_check(screen):
    template = cv2.imread(legion_approaching_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Legion Approaching popup found, clicking X!")
        move_and_click(legion_approaching_pos)
        time.sleep(1)
    except:
        pass


def legion_defeated_check(screen):
    template = cv2.imread(legion_defeat_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Legion defeated popup found, clicking X!")
        secure_click(legion_defeat_pos, anchor, 1)
        time.sleep(1)
    except:
        pass


def achievement_check(screen):
    template = cv2.imread(achievements_img, cv2.IMREAD_GRAYSCALE)
    #screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= threshold)
    try:
        test = fres[0][0] > 0
        print("Achievement popup found, clicking X!")
        secure_click(achievements_pos, anchor, 1)
        time.sleep(1)
    except:
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

  
def refresh_grab(x=200, y=500, w=1000, l=700, save=True):
    new_cord = (x, y, w, l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("tmp_refresh.png", 'PNG')
        params = ['mogrify', 'tmp_refresh.png', 'tmp_refresh.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def cancel_grab(x=200, y=300, w=1000, l=800, save=True):
    new_cord = (x, y, w, l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("tmp_cancel.png", 'PNG')
        params = ['mogrify', 'tmp_cancel.png', 'tmp_cancel.png']
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


def segment_grab_custom(cord, tag):
    x, y, w, l = cord
    im = ImageOps.grayscale(ImageGrab.grab(cord))
    filename = "segment_{}.jpg".format(tag)
    im.save(filename, 'JPEG')
    params = ['mogrify', filename, filename]
    subprocess.check_call(params, stderr=open(os.devnull, 'wb'))


def popup_grab(x=400,y=250 , w=1000, l=600, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("popup.png", 'PNG')
        params = ['mogrify', 'popup.png', 'popup.png']
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
    if y < 160:
        return
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
    segment = cv2.imread("save_segment.png", cv2.IMREAD_GRAYSCALE)
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
        cord = (int(fres[1]), int(fres[0]))
        print("Popup Anchor Found @ : {}".format(cord))
        return cord        


def is_ready():
    """ Check if a building is working """
    threshold = 0.85
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


def cycle():
    print("Running Cycle")
    move_and_click((763, 42)) #Focus Frame
    n = 4
    refresh_checker()
    navy('bottom_right', 6)
    time.sleep(2)
    move_and_click((1050, 436), 10) # Starting Position for bottom right boar farm
    time.sleep(0.2)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('top_left', 6)
    time.sleep(2)
    move_and_click((449, 340), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('bottom_left', 6)
    time.sleep(2)
    move_and_click((681, 752), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type(n)
    refresh_checker()
    navy('top_right', 6)
    time.sleep(2)
    move_and_click((1096, 552), 10)
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
    print("Starting Fishing now!")
    refresh_checker()
    navy('top_left', 4)
    secure_click((447, 340), anchor, 20) #Top left Start
    secure_click((368, 292), anchor, 5) # Fish spot top left 1
    secure_click((600, 316), anchor, 5) # Fish spot top left 2
    secure_click((592, 666), anchor, 5) # Fish spot top left 3
    secure_click((665, 861), anchor, 5) # Fish spot top left 4 - Probably wrong

    refresh_checker()
    navy('bottom_left', 4)
    secure_click((1091, 791), anchor, 5) # bottom_left Start
    secure_click((1123, 771), anchor, 5) # Fish bottom_left left 1
    secure_click((1178, 635), anchor, 5) # Fish bottom_left left 2
    secure_click((754, 386), anchor, 5) # Fish bottom_left left 3
    secure_click((796, 156), anchor, 5) # Fish bottom_left left 4 - Probably wrong
    
    refresh_checker()
    navy('top_right', 4)
    secure_click((261, 319), anchor, 5) # top_right Start
    secure_click((154, 253), anchor, 4) # Fish top_right left 1
    secure_click((324, 264), anchor, 4) # Fish top_right left 2
    secure_click((536, 231), anchor, 4) # Fish top_right left 2
    secure_click((723, 236), anchor, 4) # Fish top_right left 3
    secure_click((1004, 224), anchor, 4) # Fish top_right left 4 - Probably wrong


def secure_click(cord, anchor='', delay=0.2):
    mousePos(cord)
    time.sleep(0.2)
    mousePos(cord)
    time.sleep(0.2)
    move_and_click(cord, delay)


def secure_mouse_over(cord, anchor='', delay=0.2):
    print(cord)
    mousePos(cord)
    time.sleep(0.2)
    mousePos(cord)
    time.sleep(0.2)


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
    # asd
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
    cycle()
    time.sleep(3)


if __name__ == '__main__':
    #segment_grab(trs_x, trs_y, trs_w, trs_h, True)
    anchor = get_anchor()
    #refresh_checker()
    #get_anchored_cursor(anchor)
    multi_window_run()
    #fish_path()
    #collect_path()
    #cycle()
    