import subprocess
import os
import time
from subprocess import Popen
import psutil
import toml
from az_code import *
from pynput.keyboard import Key, Controller

fn = '.ctrltmp'
config = toml.load(fn)

launch_falkon = ['falkon', '&>/dev/null']

class Launch():
	def __init__(self):
		pass


	def checkIfProcessRunning(self, processName):
		'''
		Check if there is any running process that contains the given name processName.
		'''
		#Iterate over the all the running process
		for proc in psutil.process_iter():
			try:
				# Check if process name contains the given name string.
				#print(proc)
				if processName.lower() in proc.name().lower():
					out = str(proc)
					out = out.split('(')
					out = out[1].split(',')
					out = out[0].split('=')
					print("Found: {} @ pid: {}".format(processName, out[1]))
					return int(out[1])
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				print("Couldn't find process: {}".format(processName))
				pass
		return False;


	def unmaximise(self):
	    keyboard = Controller()
	    keyboard.press(Key.alt)
	    keyboard.press(Key.f10)
	    keyboard.release(Key.alt)
	    keyboard.release(Key.f10)


	def runFalkon(self):
		try:
			pid = self.checkIfProcessRunning('falkon')
			if pid == False:
				p = Popen(launch_falkon) # something long running
				pid = self.checkIfProcessRunning('falkon')
				print("Falkon not running, Booting now and waiting 15s")
				time.sleep(15)
			else:
				print("Falkon already open")
			self.configWriter(pid)
		except:
			print("Couldn't start Falkon or retrieve PID")
			return False


	def killFalkon(self):
		config = toml.load(fn)
		params = ['kill', '-9', str(config['process']['pid'])]
		subprocess.check_call(params, stderr=open(os.devnull, 'wb'))


	def configWriter(self, pid):
		config = toml.load(fn)
		config['process']['pid'] = pid
		with open(fn, 'w') as f:
			toml.dump(config, f)
		print("Wrote pid {} to config".format(pid))


	def resize_window(self):
		# wmctrl -r 'Asterix' -e 0,0,0,1645,870
		move_and_click((1886, 42), 1)
		time.sleep(5)
		params = ['wmctrl', '-r', 'Asterix', '-e', '0,0,0,1645,870']
		subprocess.check_call(params, stderr=open(os.devnull, 'wb'))
		print("Window resized!")


	def launch_sequence(self):
		self.runFalkon()
		self.resize_window()


if __name__ == '__main__':
	l = Launch()
	l.launch_sequence()