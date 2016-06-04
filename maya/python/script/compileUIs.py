#######################################
# imports

import maya.cmds as cmds
import pysideuic as pui
import os

import esa.maya.python.lib.io as io

reload(io)

#######################################
# attributes

permission = "developer"

#######################################
# functionality

def compileAllUis(p_sInitPath):
	sDirFiles = os.listdir(p_sInitPath)
	for sFile in sDirFiles:
		if (os.path.splitext(sFile)[1] == ".ui"):
			sUiFile = os.path.join(p_sInitPath, sFile) 
			sPyUiFilePath = os.path.join(p_sInitPath, ((os.path.splitext(sFile)[0]) + "_ui.py"))
			# print sUiFile
			# print sPyUiFilePath
			fPyUiFile = open(sPyUiFilePath, "w")
			pui.compileUi(sUiFile, fPyUiFile)
			fPyUiFile.close()
	
	sSubdirs = io.getImmediateSubdirectories(p_sInitPath)
	for sPath in sSubdirs:
		compileAllUis(sPath)

def compileUIsRun():
	currPath = os.path.dirname(os.path.dirname(__file__))
	compileAllUis(currPath)

#######################################
# execution

if __name__ == "__main__": compileUIsRun()