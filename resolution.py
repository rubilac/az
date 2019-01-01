import json
import os
from az_code import load_file


def fix_json(filename):
	data = load_file(filename)
	data_set = data['sequence']['loc']
	list_of_boars = []
	list_of_fish = []
	for loc in data_set:
		list_of_boars.append(loc['boars'])
		list_of_fish.append(loc['fish'])
	for boar in list_of_boars:
		for spawn in boar:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = spawn['start_point']['x']
			spawn['start_point']['y'] = spawn['start_point']['y']
			for s in spawn_list:
				s['y'] = s['y']
				s['x'] = s['x']
	for fish in list_of_fish:
		for spawn in fish:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = spawn['start_point']['x']
			spawn['start_point']['y'] = spawn['start_point']['y']
			for s in spawn_list:
				s['y'] = s['y']
				s['x'] = s['x']
	with open('fixed_cords.json','w') as outfile:
		json.dump(data, outfile)


def adjust_resolution(file_name, dr_x, dr_y, er_x, er_y):
	data = load_file(file_name)
	data_set = data['sequence']['loc']
	diff_x = get_diff_x(dr_x, er_x)
	diff_y = get_diff_y(dr_y, er_y)
	list_of_boars = []
	list_of_fish = []
	for loc in data_set:
		list_of_boars.append(loc['boars'])
		list_of_fish.append(loc['fish'])
	for boar in list_of_boars:
		for spawn in boar:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = int(spawn['start_point']['x']*diff_x)
			spawn['start_point']['y'] = int(spawn['start_point']['y']*diff_y+32-1080)
			for s in spawn_list:
				s['y'] = int(s['y']*diff_y+32-1080)
				s['x'] = int(s['x']*diff_x)
	for fish in list_of_fish:
		for spawn in fish:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = int(spawn['start_point']['x']*diff_x)
			spawn['start_point']['y'] = int(spawn['start_point']['y']*diff_y+32-1080)
			for s in spawn_list:
				s['y'] = int(s['y']*diff_y+32-1080)
				s['x'] = int(s['x']*diff_x)
	new_file = "spawn_{}_{}.json".format(dr_x, dr_y)
	with open(new_file, 'w') as outfile:
		json.dump(data, outfile)


def get_diff_x(dr_x, er_x):
	#desired = 900
	#existing = 1440
	data = dr_x / er_x
	print(data)
	return data


def get_diff_y(dr_y, er_y):
	#desired = 1440
	#existing = 2560
	data = dr_y / er_y
	print(data)
	return data


if __name__ == '__main__':
	dr_x = 1920
	dr_y = 1080
	er_x = 2560
	er_y = 1440
	adjust_resolution('spawn_fs_2560_1440.json', dr_x, dr_y, er_x, er_y)
	
