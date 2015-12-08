#######################################
# imports

import maya.cmds as cmds

#######################################
# functionality

def unitsConvertInternalToUI(value):
	unit = cmds.currentUnit(q=True, l=True)
	factor = 1.0

	if unit == "in": factor = 0.393700787
	elif unit == "ft": factor = 0.032808399
	elif unit == "yd": factor = 0.010936133
	elif unit == "mi": factor = 0.000006214
	elif unit == "mm": factor = 10.000000000
	elif unit == "km": factor = 0.000010000
	elif unit == "m": factor = 0.010000000

	return (value*factor)

def unitsConvertUItoInternal(value):
	unit = cmds.currentUnit(q=True, l=True)
	factor = 1.0

	if unit == "in": factor = 2.540000000
	elif unit == "ft": factor = 30.480000000
	elif unit == "yd": factor = 91.440000000
	elif unit == "mi": factor = 160934.400000000
	elif unit == "mm": factor = 0.100000000
	elif unit == "km": factor = 100000.000000000
	elif unit == "m": factor = 100.000000000

	return (value*factor)

#######################################
# execution

if __name__ == "__main__":
	# print (unitsConvertUItoInternal(12.5656))
	pass