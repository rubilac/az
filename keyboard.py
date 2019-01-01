from pynput.keyboard import Key, Controller
import time



def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
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

# Collect events until released
if __name__ == '__main__':
	time.sleep(2)
	swap_windows()