#######################################
# imports

#######################################
# functionality

def getLongestCommonSubstr(data):
	substr = ''
	if len(data) > 1 and len(data[0]) > 0:
		for i in range(len(data[0])):
			for j in range(len(data[0])-i+1):
				if j > len(substr) and all(data[0][i:i+j] in x for x in data):
					substr = data[0][i:i+j]
	return substr

#######################################
# execution

if __name__ == "__main__":
	# print getLongestCommonSubstr(["hello, how are you", "by, how are you going too?"])
	pass