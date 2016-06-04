#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys
import os

from PySide import QtCore, QtGui
from mpc import jobtools as jobTls

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.gif as gif
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.io as io

reload(utils)
reload(gif)
reload(ui)
reload(io)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class PlayblastToGIF(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(PlayblastToGIF, self).__init__(parent)
		
		self.setObjectName('playblastToGIF')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Playblast to GIF creator")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = PlayblastToGIFMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class PlayblastToGIFMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(PlayblastToGIFMainWidget, self).__init__(parent)
		self.initUI()

	def initUI(self):
		# self.setMinimumSize(200, 100)

		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

		# fill UI info
		isValid = self.isValidContext()
		if isValid:
			self.ui.cb_job.addItem(jobTls.jobName())
			self.ui.cb_scene.addItem(jobTls.sceneName())
			self.ui.cb_shot.addItem(jobTls.shotName())
			self.ui.cb_playblast.addItems(self.getCurrentJobPlayblastPathsShot())
			self.ui.cb_colors.addItems(["256", "128", "64", "32", "16", "8"])
			self.ui.cb_colors.setCurrentIndex(1)
		else:
			self.ui.setEnabled(False)
			cmds.confirmDialog(t="Alert", message="You must job in a shot to use this tool", button=["OK"], icon="warning")
		
		# add signals to the ui elements
		self.ui.pb_createGIF.clicked.connect(self.createGIF)

	def isValidContext(self):
		return (self.getCurrentJobPlayblastPath() is not None)

	def getCurrentJobPlayblastPath(self):
		jobName = jobTls.jobName()
		sceneName = jobTls.sceneName()
		shotName = jobTls.shotName()
		
		if jobName and sceneName and shotName:
			return ("/jobs/" + jobName + "/" + sceneName + "/" + shotName + "/maya/playblasts/")
		else:
			return None

	def getCurrentJobPlayblastPaths(self):
		pbPaths = []
		pbPath = self.getCurrentJobPlayblastPath()
		
		if pbPath is not None:
			pbPaths = io.getImmediateSubfolders(pbPath)

		return pbPaths

	def getCurrentJobPlayblastPathsShot(self):		
		pbPaths = self.getCurrentJobPlayblastPaths()
		pbPathsShort = []

		for pth in pbPaths:
			pbPathsShort.append(os.path.basename(pth))

		pbPathsShort.sort()

		return pbPathsShort

	def createGIF(self):
		# builds the path
		playblastPath = "/jobs/" + self.ui.cb_job.currentText() + "/" + self.ui.cb_scene.currentText() + "/" + self.ui.cb_shot.currentText() + "/maya/playblasts/" + self.ui.cb_playblast.currentText()

		# open at end mode
		openAtEnd = None
		if self.ui.rb_firefox.isChecked(): openAtEnd = "firefox"
		elif self.ui.rb_folder.isChecked(): openAtEnd = "folder"

		answer = cmds.confirmDialog(t="Alert", message="This process could take a long depending on the number of frames, the background changing and the area of animation. Do you want to continue?", button=["Cancel", "Yes"], icon="warning")

		# if we choose to continue
		if answer == "Yes":
			# creates the gif
			cmds.waitCursor(state=True)
			gif.createGIFanimFromPlayblast(playblastPath, scale=(self.ui.sp_scale.value()/100.0), colors=(int(self.ui.cb_colors.currentText())), openAtEndMode=openAtEnd)
			cmds.waitCursor(state=False)

			# launches a finish message
			cmds.confirmDialog(t="msg", message="GIF animation finished.", button=["OK"])

def playblastToGIFRun():
	utils.closeTool('playblastToGIF')
	dTool = PlayblastToGIF()

def playblastToGIFClose():
	utils.closeTool('playblastToGIF')
	
#######################################
# execution
if __name__ == "__main__": playblastToGIFRun()
