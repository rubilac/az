c_list = [(5,5), (10, 10), (11, 11)]
orig = (0,0)

out_list = []

x_b = 3
y_b = 3


for i in c_list:
	if len(out_list) == 0:
		prv_x, prv_y = orig
	if i[0] > prv_x+x_b or i[0] < prv_x-x_b:
		out_list.append(i)
		prv_x, prv_y = i
	else:
		print("Within bounds, not appending")
print(out_list)