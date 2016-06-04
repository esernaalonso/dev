#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils

reload(utils)

#######################################
# attributes

permission = "developer"

#######################################
# functionality

class TemplateToolDock(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(TemplateToolDock, self).__init__(parent)

		self.setLayout(QtGui.QVBoxLayout())

		self.setObjectName('templateToolDock')
		allowedAreas = ['right', 'left']
		self.dockCtrl = cmds.dockControl(label='Template Dock', area='right', content=self.objectName(), allowedArea=allowedAreas )

		self.opened = True		
		self.initUI()

	def initUI(self):
		# layout
		self.setLayout(QtGui.QVBoxLayout())
		
		# add main widget
		self.mainWiget = TemplateToolDockMainWiget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)

		self.show()

	def closeEvent(self, event):
		self.opened = False
		cmds.deleteUI(self.dockCtrl)

class TemplateToolDockMainWiget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(TemplateToolDockMainWiget, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.setMinimumWidth(200)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().setSpacing(4)

def templateToolDockRun():
	utils.closeTool('templateToolDock', dock=True)
	dTool = TemplateToolDock()

def templateToolDockClose():
	utils.closeTool('templateToolDock', dock=True)

#######################################
# execution
if __name__ == "__main__": templateToolDockRun()