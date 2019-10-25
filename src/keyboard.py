from pynput.keyboard import Key, Controller
from pynput import keyboard
import time
import sys



def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
        return key.char
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def swap_windows():
	keyboard = Controller()
	keyboard.press(Key.cmd)
	keyboard.press('`')
	keyboard.release('`')
	keyboard.release(Key.cmd)


def listen():
    quit_list = ["q"]
    with keyboard.Listener(on_press = on_press,
                           on_release = on_release) as listener:
        print(on_press, on_release)
        if on_release in quit_list or on_press in quit_list:
            sys.exit()
    time.sleep(25)


# Collect events until released
if __name__ == '__main__':
    listen()