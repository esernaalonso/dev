#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.bake as bake
import esa.maya.python.lib.mpcRig as mpcRig

reload(utils)
reload(ui)
reload(bake)
reload(mpcRig)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class BakeACPdynamics(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(BakeACPdynamics, self).__init__(parent)
		
		self.setObjectName('bakeACPdynamics')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Bake ACP dynamics")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = BakeACPdynamicsMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class BakeACPdynamicsMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(BakeACPdynamicsMainWidget, self).__init__(parent)
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
		self.fillSceneACPdynamicsList()
		self.useSceneFrameRange()

		# add signals to the ui elements
		self.ui.pb_toBake.clicked.connect(self.toBakeList)
		self.ui.pb_toScene.clicked.connect(self.toSceneList)
		self.ui.pb_fillFromScene.clicked.connect(self.fillListsFromSelection)
		self.ui.sb_start.editingFinished.connect(self.preserveFrameRangeValidityUp)
		self.ui.sb_end.editingFinished.connect(self.preserveFrameRangeValidityDown)
		self.ui.pb_reset.clicked.connect(self.useSceneFrameRange)
		self.ui.pb_bake.clicked.connect(self.bake)

	def useSceneFrameRange(self):
		self.ui.sb_start.setValue(int(cmds.playbackOptions(q=True, minTime=True)))
		self.ui.sb_end.setValue(int(cmds.playbackOptions(q=True, maxTime=True)))

	def preserveFrameRangeValidityUp(self):
		if self.ui.sb_start.value() > self.ui.sb_end.value(): self.ui.sb_end.setValue(self.ui.sb_start.value())

	def preserveFrameRangeValidityDown(self):
		if self.ui.sb_end.value() < self.ui.sb_start.value(): self.ui.sb_start.setValue(self.ui.sb_end.value())

	def fillSceneACPdynamicsList(self):
		self.ui.lw_sceneACPdynamics.clear()
		self.ui.lw_bakeACPdynamics.clear()
		sceneDynamics = mpcRig.getSceneACPdynamicSystemsNames()
		for dynSys in sceneDynamics: self.ui.lw_sceneACPdynamics.addItem(dynSys)

	def fillListsFromSelection(self):
		self.ui.lw_sceneACPdynamics.clear()
		self.ui.lw_bakeACPdynamics.clear()

		sceneDynamics = mpcRig.getSceneACPdynamicSystemsNames()
		sceneDynamicsSelected = mpcRig.getSceneACPdynamicSystemsNames(selection=True)
		sceneDynamics = list(set(sceneDynamics) - set(sceneDynamicsSelected))

		for dynSys in sceneDynamics: self.ui.lw_sceneACPdynamics.addItem(dynSys)
		for dynSys in sceneDynamicsSelected: self.ui.lw_bakeACPdynamics.addItem(dynSys)

	def toBakeList(self):
		sel = self.ui.lw_sceneACPdynamics.selectedItems()
		for i in range(len(sel)):
			self.ui.lw_bakeACPdynamics.addItem(sel[i].text())
			self.ui.lw_sceneACPdynamics.takeItem(self.ui.lw_sceneACPdynamics.row(sel[i]))

	def toSceneList(self):
		sel = self.ui.lw_bakeACPdynamics.selectedItems()
		for i in range(len(sel)):
			self.ui.lw_sceneACPdynamics.addItem(sel[i].text())
			self.ui.lw_bakeACPdynamics.takeItem(self.ui.lw_bakeACPdynamics.row(sel[i]))

	def bake(self):
		ACPnames = []
		dynSysNames = []

		for i in range(self.ui.lw_bakeACPdynamics.count()):
			itemText = self.ui.lw_bakeACPdynamics.item(i).text()
			nameParts = itemText.split(":")

			ACPname = itemText.replace((":" + nameParts[len(nameParts) - 1]), "")
			dynSysName = nameParts[len(nameParts) - 1]
			
			if ACPname not in ACPnames: ACPnames.append(ACPname)
			if dynSysName not in dynSysNames: dynSysNames.append(dynSysName)

		if len(ACPnames) > 0 and len(dynSysNames) > 0:
			answer = cmds.confirmDialog(t="Alert", message="This process has no undo. Do you want to continue?", button=["Cancel", "Yes"], icon="warning")
			if answer == "Yes":
				start = self.ui.sb_start.value()
				end = self.ui.sb_end.value()
				bake.bakeACPdynamics(ACPnames, dynSysNames, start, end, timeStep=1, startingControl=1)
				self.fillSceneACPdynamicsList()

def bakeACPdynamicsRun():
	utils.closeTool('bakeACPdynamics')
	dTool = BakeACPdynamics()

def bakeACPdynamicsClose():
	utils.closeTool('bakeACPdynamics')
	
#######################################
# execution
if __name__ == "__main__": bakeACPdynamicsRun()