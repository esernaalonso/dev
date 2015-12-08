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

class TemplateToolStd(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(TemplateToolStd, self).__init__(parent)
		
		self.setObjectName('templateToolStd')
		self.opened = True
		
		self.initUI()

	def initUI(self):		
		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = TemplateToolStdMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class TemplateToolStdMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(TemplateToolStdMainWidget, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.setMinimumSize(200, 100)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().setSpacing(4)

def templateToolStdRun():
	utils.closeTool('templateToolStd')
	dTool = TemplateToolStd()

def templateToolStdClose():
	utils.closeTool('templateToolStd')
	
#######################################
# execution
if __name__ == "__main__": templateToolStdRun()