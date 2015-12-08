#######################################
# imports

import os

from PySide import QtCore, QtGui

#######################################
# functionality

def getIconsPath():
	return (os.path.dirname(os.path.dirname(__file__)) + "/icon")

def getIconByName(iconName):
	# icon = QtGui.QIcon((getIconsPath() + iconName))

	# icon = QtGui.QIcon(QtGui.QStyle.SP_DialogOpenButton)
	iconFile = getIconsPath() + "/" + iconName
	# print iconFile
	icon = QtGui.QIcon(iconFile)
	# icon.addPixmap(QtGui.QPixmap(iconFile),QtGui.QIcon.Normal,QtGui.QIcon.Off)

	return icon

#######################################
# execution

if __name__ == "__main__":
	print getIconByName("folder_16x16.png")
	pass