#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys
import shiboken
import ntpath
import importlib

from PySide import QtCore, QtGui
from shiboken import wrapInstance

import esa.maya.python.lib.inspector as inspector
import esa.maya.python.lib.main as main

reload(main)
reload(inspector)

#######################################
# functionality

def getMayaWindow():
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return wrapInstance(long(ptr), QtGui.QMainWindow)

def mayaWindowToPySideWidget(mayaName):
	ptr = apiUI.MQtUtil.findControl(mayaName)
	if ptr is None: ptr = apiUI.MQtUtil.findLayout(mayaName)
	if ptr is None: ptr = apiUI.MQtUtil.findMenuItem(mayaName)

	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget)
	else:
		return None

def isToolOpened(toolName):
	mayaWindow = getMayaWindow()
	oTool = mayaWindow.findChild(QtGui.QDialog, toolName)

	if oTool and hasattr(oTool, "opened"): return oTool.opened
	else: return False

def isToolDockable(toolName):
	mayaWindow = getMayaWindow()
	oTool = mayaWindow.findChild(QtGui.QDialog, toolName)

	if oTool and hasattr(oTool, "dockCtrl"): return True
	else: return False

def closeTool(toolName, dock=False):
	mayaWindow = getMayaWindow()
	tool = mayaWindow.findChild(QtGui.QDialog, toolName)
	if tool:
		if (not dock):
			shiboken.delete(tool)
		else:
			tool.close()

		tool = None

def getTool(toolName):
	mayaWindow = getMayaWindow()
	return mayaWindow.findChild(QtGui.QDialog, toolName)

def openTool(toolName, module=None):
	if module == None: module = mayaWindow.findChild(QtGui.QDialog, toolName)
	if module == None:
		importStatement = main.getPyFileFullImportName(sToolFileName)
		module = importlib.import_module(importStatement)

	toolFunctions = inspector.getModFunctions(module)
	for tf in toolFunctions:
		if (tf == "run") or (tf.lower() == (toolName.lower() + "run")):
			getattr(module, tf)()

def executeScript(scriptName, module=None):
	if module == None: module = mayaWindow.findChild(QtGui.QDialog, scriptName)
	if module == None:
		importStatement = main.getPyFileFullImportName(sToolFileName)
		module = importlib.import_module(importStatement)

	scriptFunctions = inspector.getModFunctions(module)
	for sf in scriptFunctions:
		if (sf == "run") or (sf.lower() == (scriptName.lower() + "run")):
			getattr(module, sf)()

def getSelfToolName(file):
	return ntpath.basename(file).replace(".py", "")

#######################################
# execution

if __name__ == "__main__":
	# print "test operations"
	# print (isToolOpened("templateToolStd"))
	# print (isToolOpened("templateToolDock"))
	# print (importModule("templateToolStd"))
	pass
