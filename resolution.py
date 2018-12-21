import json
import os
from az_code import load_sequence


def fix_json(filename):
	data = load_sequence(filename)
	data_set = data['sequence']['loc']
	list_of_boars = []
	list_of_fish = []
	for loc in data_set:
		list_of_boars.append(loc['boars'])
		list_of_fish.append(loc['fish'])
	for boar in list_of_boars:
		for spawn in boar:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = spawn['start_point']['x']+979
			spawn['start_point']['y'] = spawn['start_point']['y']+356
			for s in spawn_list:
				s['y'] = s['y']+356
				s['x'] = s['x']+979
	for fish in list_of_fish:
		for spawn in fish:
			spawn_list = spawn['spawns']
			spawn['start_point']['x'] = spawn['start_point']['x']+979
			spawn['start_point']['y'] = spawn['start_point']['y']+356
			for s in spawn_list:
				s['y'] = s['y']+356
				s['x'] = s['x']+979
	with open('fixed_cords.json','w') as outfile:
		json.dump(data, outfile)

if __name__ == '__main__':
	fix_json('spawn_fs_2560_1440.json')
