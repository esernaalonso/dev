#######################################
# imports

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
import sys

from PySide import QtCore, QtGui
from mpc import jobtools as jobTls

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.shader as shader

reload(utils)
reload(ui)
reload(shader)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class ProjectionManager(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(ProjectionManager, self).__init__(parent)
		
		self.setObjectName('projectionManager')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Projection Manager")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = ProjectionManagerMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class ProjectionManagerMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ProjectionManagerMainWidget, self).__init__(parent)
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
			self.ui.cb_imagePlanes.addItems(shader.getAllSceneImagePlanes())
		else:
			self.ui.setEnabled(False)
			cmds.confirmDialog(t="Alert", message="There are no ImagePlanes in the scene, there must be one at least.", button=["OK"], icon="warning")
		
		# add signals to the ui elements
		self.ui.pb_bakeImagePlane.clicked.connect(self.bakeImagePlane)
		self.ui.pb_useBackgroundShader.clicked.connect(self.applyUseBackgroundShader)
		self.ui.pb_lambertProjection.clicked.connect(self.applyLambertShader)
		self.ui.pb_surfaceShader.clicked.connect(self.applySurfaceShader)
		self.ui.pb_applyGreenScreenShader.clicked.connect(self.applyGreenScreenShader)
		self.ui.pb_applyGreenScreenShaderFx.clicked.connect(self.applyGreenScreenShaderFx)
		self.ui.pb_applyDefaultShader.clicked.connect(self.applyDefaultShader)

	def isValidContext(self):
		return (len(shader.getAllSceneImagePlanes()) > 0)

	def bakeImagePlane(self):
		# find the camera related with the selected image plane in the ui and select it
		camName = ((self.ui.cb_imagePlanes.currentText()).split("->")[0].replace("Shape", ""))
		cmds.select(camName)

		# convert to geometry card
		mel.eval('source "/jobs/layout_dept/tools/maya/geoCardFromImgPlane.mel";')
		mel.eval('geoCardFromImgPlane_doIt("' + self.ui.cb_imagePlanes.currentText() + '");')

		# disable the image plane to leave only the geo card visible
		cmds.setAttr((self.ui.cb_imagePlanes.currentText() + ".displayMode"), lock=False)
		cmds.setAttr((self.ui.cb_imagePlanes.currentText() + ".displayMode"), 0)

		# get the baked planes and apply to them a surface shader
		bakedPlanes = cmds.ls( 'imagePlaneGeoCardBaked*', transforms=True)
		shader.applySurfaceBackgroundShader(bakedPlanes, self.ui.cb_imagePlanes.currentText())

	def applyUseBackgroundShader(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applyUseBackgroundShader(jobObjects)

	def applyLambertShader(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applyLambertBackgroundShader(jobObjects, self.ui.cb_imagePlanes.currentText())

	def applySurfaceShader(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applySurfaceBackgroundShader(jobObjects, self.ui.cb_imagePlanes.currentText())

	def applyGreenScreenShader(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applyGreenScreenShader(jobObjects)

	def applyGreenScreenShaderFx(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applyGreenScreenShaderFx(jobObjects)
	
	def applyDefaultShader(self):
		jobObjects = self.getCurrentSelection()

		if len(jobObjects) > 0:
			shader.applyDefaultShader(jobObjects)

	def getCurrentSelection(self):
		currSel = cmds.ls(selection=True)
		if len(currSel) == 0:
			cmds.confirmDialog(t="Alert", message="No objects selected. Select one at least to apply shader.", button=["OK"], icon="warning")

		return currSel

def projectionManagerRun():
	utils.closeTool('projectionManager')
	dTool = ProjectionManager()

def projectionManagerClose():
	utils.closeTool('projectionManager')
	
#######################################
# execution
if __name__ == "__main__": projectionManagerRun()