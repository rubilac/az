from PIL import ImageGrab
import os
import time
import json
import datetime
from az_code_mac import *
from az_crafting import *
from PIL import ImageOps
from numpy import *
import numpy as np
import timeit
import cv2
import warnings
import subprocess
from keyboard import *

trs_x = 1*2
trs_y = 1*2
trs_w = 1200*2
trs_h = 1200*2
method = cv2.TM_CCOEFF_NORMED
threshold = 0.90


template_path_boar = '/opt/dev/az/templates/boar/'
load_boars = os.listdir(template_path_boar)
boar_templates_loaded = []
for boar_tmp in load_boars:
    boar_tmp = cv2.imread(template_path_boar+boar_tmp, cv2.IMREAD_GRAYSCALE)
    boar_templates_loaded.append(boar_tmp)


# Button positions
refresh_button = (-502, 525)
decline_special_offer = (-421, 598)
ok_pos = (-440, 667)
complete_pos = (-540, 667)
sesterce_close_pos = (-168, 296)
roman_helmets_close_pos = (-170, 259)
legion_approaching_pos = (-352, 291)
legion_defeat_pos = (-587, 635)


# Image locations
refresh_img = '/opt/dev/az/templates/popups/refresh.png'
special_offer_img = '/opt/dev/az/templates/popups/special_offer.png'
ok_img = '/opt/dev/az/templates/popups/ok.png'
complete_img = '/opt/dev/az/templates/popups/complete.png'
sesterce_img = '/opt/dev/az/templates/popups/sesterce.png'
roman_helmets_img = '/opt/dev/az/templates/popups/roman_helmets.png'
legion_approaching_img = '/opt/dev/az/templates/popups/legion_approaching.png'
legion_defeat_img = '/opt/dev/az/templates/popups/legion_defeated.png'


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


def is_popup():
    """ Check if a popup exists """
    popup_grab()
    screen = cv2.imread("popup.png", cv2.IMREAD_GRAYSCALE)
    threshold = 0.97
    popup_exists = False
    refresh_check()
    special_offer_check(screen)
    ok_check(screen)
    quest_complete_check(screen)
    get_more_sesterce_check(screen)
    get_more_roman_helmets_check(screen)
    legion_approaching_check(screen)
    legion_defeated_check(screen)


def refresh_check():
    template = cv2.imread(refresh_img)
    refresh_grab()
    screen = cv2.imread('tmp_refresh.png')
    result = cv2.matchTemplate(screen, template, method)
    fres = np.where(result >= 0.98)
    try:
        test = fres[0][0]>0
        print("Refresh Button Found. Waiting 5s before clicking...")
        time.sleep(2)
        try:
            #print(refresh_button)
            secure_click(refresh_button, anchor, 1)
        except:
            print("sad")
        print("Clicked Refresh, waiting 20s for before continuing")
        time.sleep(20)
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
        secure_click((-417, 543), anchor, 1)
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
        secure_click(legion_approaching_pos, anchor, 1)
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


def segment_grab(x, y, w, l, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("segment.png", 'PNG')
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


def popup_grab(x=200*2,y=300*2 , w=1500, l=1200, save=True):
    new_cord = (x, y, x+w, y+l)
    im = ImageOps.grayscale(ImageGrab.grab(new_cord))
    if save:
        im.save("popup.png", 'PNG')
        params = ['mogrify', 'popup.png', 'popup.png']
        subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
    else:
        return im


def refresh_grab(x=500*2, y=500*2, w=800*2, l=900*2, save=True):
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
        cursor_grab_color(w, h, num)
        num -= 1
        time.sleep(timer)


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


def get_anchor():
    """ Get the cords of the anchor """
    threshold = 0.99
    segment = cv2.imread("segment.png", cv2.IMREAD_GRAYSCALE)
    try:
        template = cv2.imread("/opt/dev/az/templates/anchor.png", cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(segment, template, method)
        fres = np.where(result >= threshold)
        cord = (int(fres[1]/2), int(fres[0]/2))
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
    threshold = 0.99
    segment = cv2.imread("town.png", cv2.IMREAD_GRAYSCALE)
    template = cv2.imread("/opt/dev/az/templates/ready.png", cv2.IMREAD_GRAYSCALE)
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
    n = 4
    is_popup()
    navy('bottom_right', 6)
    time.sleep(2)
    mousePos((672, 730))
    time.sleep(0.2)
    move_and_click((672, 730), 10)
    time.sleep(0.2)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    is_popup()
    navy('bottom_left', 6)
    time.sleep(2)
    move_and_click((762, 978), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    is_popup()
    navy('top_right', 6)
    time.sleep(2)
    move_and_click((935, 702), 10)
    for i in range(n):
        print("Starting round {}".format(i))
        clear_segment_type_3(n)
    fish_path()


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
    is_popup()
    navy('top_left', 6)
    mousePos(anchor_convert(anchor,(-608, 262)))
    move_and_click(anchor_convert(anchor,(-608, 262)), 20) #Top left Start
    mousePos(anchor_convert(anchor, (-721, 180)))
    move_and_click(anchor_convert(anchor, (-721, 180)), 5)
    mousePos(anchor_convert(anchor, (-455, 206)))
    move_and_click(anchor_convert(anchor, (-455, 206)), 5)
    mousePos(anchor_convert(anchor, (-478, 639)))
    move_and_click(anchor_convert(anchor, (-478, 639)), 5)
    mousePos(anchor_convert(anchor, (-381, 901)))
    move_and_click(anchor_convert(anchor, (-381, 901)), 5)
    is_popup()
    navy('bottom_left', 6)
    move_screen_right(2, 300)
    mousePos(anchor_convert(anchor, (-434, 801)))
    move_and_click(anchor_convert(anchor,(-434, 801)), 15) #Middle Bottom Start
    mousePos(anchor_convert(anchor, (-396, 773)))
    move_and_click(anchor_convert(anchor, (-396, 765)), 5)
    mousePos(anchor_convert(anchor, (-328, 600)))
    move_and_click(anchor_convert(anchor, (-328, 600)), 5)
    mousePos(anchor_convert(anchor, (-854, 292)))
    move_and_click(anchor_convert(anchor, (-854, 280)), 8)
    move_screen_up(4, 300)
    mousePos(anchor_convert(anchor, (-780, 681)))
    move_and_click(anchor_convert(anchor,(-780, 681)), 15) #Middle Top Start
    mousePos(anchor_convert(anchor, (-803, 406)))
    move_and_click(anchor_convert(anchor, (-803, 406)), 5)
    mousePos(anchor_convert(anchor, (-722, 128)))
    move_and_click(anchor_convert(anchor, (-722, 128)), 5)
    mousePos(anchor_convert(anchor, (-488, 152)))
    move_and_click(anchor_convert(anchor, (-488, 152)), 5)
    mousePos(anchor_convert(anchor, (-213, 105)))
    move_and_click(anchor_convert(anchor, (-213, 105)), 5)
    is_popup()
    navy('top_right', 6)
    time.sleep(2)
    mousePos(anchor_convert(anchor, (-480, 178)))
    move_and_click(anchor_convert(anchor,(-480, 178)), 15) #Top right Start    
    mousePos(anchor_convert(anchor, (-473, 97)))
    move_and_click(anchor_convert(anchor, (-473, 97)), 5)
    mousePos(anchor_convert(anchor, (-836, 106)))
    move_and_click(anchor_convert(anchor, (-836, 106)), 5)


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
    is_popup()
    navy('top_right', 4)
    secure_click((15, 162), anchor, 1)
    secure_click((-1025, 634), anchor, 1)
    secure_click((-942, 543), anchor, 1)
    secure_click((-832, 595), anchor, 1)
    is_popup()
    navy('bottom_right', 2)
    secure_click((-178, 694), anchor, 1)
    move_screen_left(2, 300)
    secure_click((-592, 860), anchor, 1)
    secure_click((-178, 694), anchor, 1)
    is_popup()
    navy('bottom_left', 2)
    secure_click((-814, 815), anchor, 1)
    is_popup()
    navy('top_left', 3)
    secure_click((-830, 468), anchor, 1)
    secure_click((-530, 294), anchor, 1)


def anchor_convert(anchor, cord):
    return (anchor[0]+cord[0], anchor[1]+cord[1])


def multi_window_run():
    print("Running Cycle")
    cycle()
    time.sleep(3)
    print('Collecting RP!')
    collect_path()

if __name__ == '__main__':
    anchor = get_anchor()
    #get_anchored_cursor(anchor)
    is_popup()
    multi_window_run()
    #refresh_check()
    #fish_path()
    #collect_path()
    #segment_grab(trs_x, trs_y, trs_w, trs_h, True)