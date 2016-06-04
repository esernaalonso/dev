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
		p_recSubfolders += getRecursiveSubdfolders(p)

	return p_recSubfolders

def initPlugin(invert=False):
	pluginFolder = cmds.about(preferences=True) + "/modules/<pluginName>"

	if not invert:
		if not pluginFolder in sys.path: sys.path.append(pluginFolder)
	else:
		if pluginFolder in sys.path: sys.path.remove(pluginFolder)

def createPluginMenu():
	mel.eval("global string $gMainWindow;")
	mel.eval("setParent $gMainWindow;")
	mel.eval('global string $g<pluginName> = "<pluginName>";')
	mel.eval("if (`menu -ex $g<pluginName>`) {deleteUI -menu $g<pluginName>;}")
	mel.eval('menu -label "<pluginName>" -allowOptionBoxes true -tearOff true $g<pluginName>;')
	mel.eval("menuItem -label \"<pluginName>\" -c \"python(\\\"import <pluginName>.<pluginName>Launcher as <pluginName>Launcher; <pluginName>Launcher.run()\\\")\";")

# Run the plugin
def run():
	initPlugin()
	createPluginMenu()

# Initialize script plugin
def initializePlugin(mobject):
	initPlugin()
	createPluginMenu()

# Uninitialize script plugin
def uninitializePlugin(mobject):
	initPlugin(invert=True)

#######################################
# execution
if __name__ == "__main__": run()