############################################################################################
# This is for loading all dev folders and subfolders to the sys path.
# This way you can import everything
#############################################################################################

#######################################
# imports

import maya.cmds as cmds
import maya.mel as mel

import os
import sys

#######################################
# functionality

def getImmediateSubfolders(p_sDir):
	return [os.path.join(p_sDir, name) for name in os.listdir(p_sDir) if (os.path.isdir(os.path.join(p_sDir, name)) and (name != ".git") and (name != ".svn"))]

def getRecursiveSubdfolders(p_sDir):
	p_recSubfolders = [p_sDir]
	p_subfolders = getImmediateSubfolders(p_sDir)

	for p in p_subfolders:
		# p_recSubfolders.append(p)
		p_recSubfolders += getRecursiveSubdfolders(p)

	return p_recSubfolders

def initDevTree(invert=False):
	p_devFolder001 = "P:\\dev"

	print "------------------------------------------------------"

	p_devFolders = []
	# p_devFolders += getRecursiveSubdfolders(p_devFolder001)
	p_devFolders += ["P:\\dev"]

	for p in p_devFolders:
		print p

		if not invert:
			if not p in sys.path: sys.path.append(p)
		else:
			if p in sys.path: sys.path.remove(p)

	print "------------------------------------------------------"

	for p in sys.path: print p

	print "------------------------------------------------------"

def createDevMenu():
	mel.eval("global string $gMainWindow;")
	mel.eval("setParent $gMainWindow;")
	mel.eval('global string $devMenu = "esa";')
	mel.eval("if (`menu -ex $devMenu`) {deleteUI -menu $devMenu;}")
	mel.eval('menu -label "ESA" -allowOptionBoxes true -tearOff true $devMenu;')
	mel.eval("menuItem -label \"Tool Manager\" -c \"python(\\\"import esa.maya.python.tool.toolManager as toolManager; toolManager.toolManagerRun()\\\")\";")

def run():
	initDevTree()
	createDevMenu()
	pass

# Initialize script plugin
def initializePlugin(mobject):
	# openPorts()
	initDevTree()
	createDevMenu()
	pass

# Uninitialize script plugin
def uninitializePlugin(mobject):
	initDevTree(invert=True)
	# closePorts()
	pass

#######################################
# execution
if __name__ == "__main__": run()