#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui

reload(utils)
reload(ui)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class NodesetManager(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(NodesetManager, self).__init__(parent)
		
		self.setObjectName('nodesetManager')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Nodeset Manager")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = NodesetManagerMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class NodesetManagerMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(NodesetManagerMainWidget, self).__init__(parent)
		self.initUI()

	def initUI(self):
		# self.setMinimumSize(200, 100)

		# load UI file
		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

def nodesetManagerRun():
	utils.closeTool('nodesetManager')
	dTool = NodesetManager()

def nodesetManagerClose():
	utils.closeTool('nodesetManager')
	
#######################################
# execution
if __name__ == "__main__": nodesetManagerRun()