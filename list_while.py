s = "string"
l = [1,2,3,4]
n = 2
if s == "not-string":
	print "not a string"
else:
	if type(l) == list:
		n = 3
		while n > 0:
			print n
			n -= 1