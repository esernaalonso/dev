#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI

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

class Renamer(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(Renamer, self).__init__(parent)
		
		self.setObjectName('renamer')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Osom Renamer")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = RenamerMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.mainWiget.killScriptJobs()
		self.opened = False		

class RenamerMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(RenamerMainWidget, self).__init__(parent)

		# init attributes
		self.updateEnabled = True
		self.currentList = []
		self.selectionChangedScriptJob = None

		# init UI
		self.initUI()

	def initUI(self):
		# self.setMinimumSize(200, 100)

		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

		# table list config
		self.ui.tw_namesList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.ui.tw_namesList.insertColumn(0)
		self.ui.tw_namesList.insertColumn(1)
		self.ui.tw_namesList.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.Stretch)
		self.ui.tw_namesList.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
		lHeaders = ["Names Before", "Names After"]
		self.ui.tw_namesList.setHorizontalHeaderLabels(lHeaders)
		self.ui.tw_namesList.verticalHeader().hide()

		# fill UI info
		self.ui.cb_operateOn.addItems(["All", "Transforms", "Geometry", "Nurbs", "Polygon Objects", "Cameras", "Joints", "ikHandles", "Sets", "Lights", "Shaders"])
		self.ui.cb_numberedOrder.addItems(["Ascending", "Descending"])
		self.ui.cb_letteredOrder.addItems(["Ascending", "Descending"])
		self.letteredStartingUpdate()
		self.fillList()

		# signals connect
		self.signalsConnect()		

		# launch start scriptJobs
		self.updateSelectionChangedScriptJob()

	def signalsConnect(self):
		self.ui.cb_operateOn.currentIndexChanged.connect(self.fillList)

		self.ui.cb_shapes.clicked.connect(self.fillList)
		self.ui.cb_selected.clicked.connect(self.updateSelectionChangedScriptJob)
		self.ui.cb_selected.clicked.connect(self.fillList)
		self.ui.cb_visible.clicked.connect(self.fillList)

		self.ui.pb_refresh.clicked.connect(self.fillList)

		self.ui.sb_removeBefore.valueChanged.connect(self.updateAfterList)
		self.ui.sb_removeAfter.valueChanged.connect(self.updateAfterList)

		self.ui.le_prefix.textChanged.connect(self.updateAfterList)
		self.ui.le_base.textChanged.connect(self.updateAfterList)
		self.ui.le_sufix.textChanged.connect(self.updateAfterList)

		self.ui.gb_numbered.toggled.connect(self.updateAfterList)
		self.ui.sb_numberedStarting.valueChanged.connect(self.updateAfterList)
		self.ui.sb_numberedDigits.valueChanged.connect(self.updateAfterList)
		self.ui.sb_numberedIncrement.valueChanged.connect(self.updateAfterList)
		self.ui.cb_numberedOrder.currentIndexChanged.connect(self.updateAfterList)

		self.ui.gb_lettered.toggled.connect(self.updateAfterList)
		self.ui.cb_letteredStarting.currentIndexChanged.connect(self.updateAfterList)

		self.ui.sb_letteredDigits.valueChanged.connect(self.letteredStartingUpdate)
		self.ui.sb_letteredDigits.valueChanged.connect(self.updateAfterList)

		self.ui.sb_letteredIncrement.valueChanged.connect(self.updateAfterList)
		self.ui.cb_letteredOrder.currentIndexChanged.connect(self.updateAfterList)
		
		self.ui.le_find.textChanged.connect(self.updateAfterList)
		self.ui.le_replace.textChanged.connect(self.updateAfterList)

		self.ui.tw_namesList.itemSelectionChanged.connect(self.updateAfterList)
		self.ui.tw_namesList.itemChanged.connect(self.renameSingleItem)

		self.ui.pb_apply.clicked.connect(self.applyNewNames)

	def renameNode(self, currentName, newName, renameChildren=False, childrenTag="Ch", renameShapes=True, shapesTag="Shp"):
		
		currNode = cmds.ls(currentName)
		if currentName != newName and (currNode is not None) and (len(currNode) > 0):
			cmds.rename(currentName, newName, ignoreShape=True)

			if renameShapes:
				shapes = cmds.listRelatives([newName], shapes=True)
				if shapes is not None:
					for i in range(len(shapes)):
						cmds.rename(shapes[i], (newName + shapesTag + str(i+1).zfill(3)))

			if renameChildren:
				children = cmds.listRelatives([newName], children=True, type="transform")
				if children is not None:
					for i in range(len(children)):
						self.renameNode(children[i], (newName + childrenTag + str(i+1).zfill(3)), renameChildren=renameChildren, childrenTag=childrenTag, renameShapes=renameShapes, shapesTag=shapesTag)

	def renameSingleItem(self, item):
		if self.updateEnabled:
			self.disableUpdate()

			renameChildren = self.ui.cb_renameChildren.isChecked()
			renameShapes = self.ui.cb_renameShapes.isChecked()

			childrenTag = self.ui.le_childrenTag.text()
			shapesTag = self.ui.le_shapesTag.text()

			currentName = self.currentList[item.row()]
			newName = item.text()

			self.renameNode(currentName, newName, renameChildren=renameChildren, childrenTag=childrenTag, renameShapes=renameShapes, shapesTag=shapesTag)

			self.ui.tw_namesList.item(item.row(), 0).setText(newName)
			self.ui.tw_namesList.item(item.row(), 1).setText(newName)

			self.currentList[item.row()] = newName

			self.enableUpdate()

	def applyNewNames(self):
		self.disableUpdate()

		renameChildren = self.ui.cb_renameChildren.isChecked()
		renameShapes = self.ui.cb_renameShapes.isChecked()

		childrenTag = self.ui.le_childrenTag.text()
		shapesTag = self.ui.le_shapesTag.text()

		for i in range(len(self.currentList)):
			currentName = self.currentList[i]
			newName = self.ui.tw_namesList.item(i, 1).text()

			self.renameNode(currentName, newName, renameChildren=renameChildren, childrenTag=childrenTag, renameShapes=renameShapes, shapesTag=shapesTag)

		self.clearUIfields()
		self.enableUpdate()
		self.fillList()

	def clearUIfields(self):
		self.ui.sb_removeBefore.setValue(0)
		self.ui.sb_removeAfter.setValue(0)
		self.ui.le_prefix.setText("")
		self.ui.le_base.setText("")
		self.ui.le_sufix.setText("")
		self.ui.le_find.setText("")
		self.ui.le_replace.setText("")

	def disableUpdate(self):
		self.updateEnabled = False

	def enableUpdate(self):
		self.updateEnabled = True

	# selectionChangedScriptJob
	def updateSelectionChangedScriptJob(self):
		if self.ui.cb_selected.isChecked():
			if self.selectionChangedScriptJob is None:
				self.selectionChangedScriptJob = cmds.scriptJob(e=["SelectionChanged", self.fillList])
		else:
			if not self.selectionChangedScriptJob is None:
				cmds.scriptJob(kill=self.selectionChangedScriptJob)
				self.selectionChangedScriptJob = None

	# Kills all scriptjobs
	def killScriptJobs(self):
		if not self.selectionChangedScriptJob is None:
			cmds.scriptJob(kill=self.selectionChangedScriptJob)
			self.selectionChangedScriptJob = None

	# get the elements that has to be shown in the list
	def getListElements(self):
		listElements = []

		showShapes = self.ui.cb_shapes.isChecked()
		onlySelected = self.ui.cb_selected.isChecked()
		onlyVisible = self.ui.cb_visible.isChecked()
		includeParents = False

		# gets all scene shape objects
		shapeElements = cmds.ls(shapes=True)
		selectedElements = cmds.ls(selection=True)
		visibleElements = cmds.ls(visible=True)

		operateOn = str(self.ui.cb_operateOn.currentText())

		if operateOn == "All":
			listElements = cmds.ls()
		elif operateOn == "Transforms":
			listElements = cmds.ls(transforms=True)
		elif operateOn == "Geometry":
			listElements = cmds.ls(geometry=True)
			includeParents = True
		elif operateOn == "Nurbs":
			listElements = cmds.ls(type="nurbsCurve")
			includeParents = True
		elif operateOn == "Polygon Objects":
			listElements = cmds.ls(type="mesh")
			includeParents = True
		elif operateOn == "Cameras":
			listElements = cmds.ls(type="camera")
			includeParents = True
		elif operateOn == "Joints":
			listElements = cmds.ls(type="joint")
		elif operateOn == "ikHandles":
			listElements = cmds.ls(type="ikHandle")
		elif operateOn == "Sets":
			listElements = cmds.ls(sets=True)
		elif operateOn == "Lights":
			listElements = cmds.ls(lights=True)
			includeParents = True
		elif operateOn == "Shaders":
			listElements = cmds.ls(materials=True)

		if includeParents:
			for elm in listElements:
				if elm in shapeElements:
					listElements.append(cmds.listRelatives(elm, parent=True)[0])
		
		if onlySelected:
			listElements = list(set(listElements) & set(selectedElements))

		if onlyVisible:
			listElements = list(set(listElements) & set(visibleElements))

		if not showShapes:
			listElements = list(set(listElements) - set(shapeElements))			

		listElements.sort()		

		return listElements

	# fills the list with the elements to rename
	def fillList(self):
		if self.updateEnabled:
			self.disableUpdate()

			# clear the list
			while self.ui.tw_namesList.rowCount() > 0:
				self.ui.tw_namesList.removeRow(0)

			# get the elements for the list
			lElements = self.getListElements()
			self.currentList = lElements

			# loops the list and fills the list
			for i in range(len(lElements)):
				# create the cells
				self.ui.tw_namesList.insertRow(i)
				self.ui.tw_namesList.setRowHeight(i, 17)
				iNameBefore = QtGui.QTableWidgetItem(lElements[i])
				iNameAfter = QtGui.QTableWidgetItem(lElements[i])
				
				# add the cells
				self.ui.tw_namesList.setItem(i, 0, iNameBefore)
				self.ui.tw_namesList.setItem(i, 1, iNameAfter)

			self.enableUpdate()
			self.updateAfterList()

	# updates the after list
	def updateAfterList(self):
		if self.updateEnabled:
			self.disableUpdate()

			rowsToUpdate = []

			if len(self.ui.tw_namesList.selectedIndexes()) > 0:
				for index in self.ui.tw_namesList.selectedIndexes():
					rowsToUpdate.append(index.row()) 
			else:
				for i in range(self.ui.tw_namesList.rowCount()):
					rowsToUpdate.append(self.ui.tw_namesList.item(i,0).row())

			rowsToUpdate = list(set(rowsToUpdate))
			# rowsToUpdate.sort()

			numbered = self.ui.gb_numbered.isChecked()
			numberedList = []
			if numbered: numberedList = self.getNumberedList(len(rowsToUpdate))
			numCount = 0

			lettered = self.ui.gb_lettered.isChecked()
			letteredList = []
			if lettered: letteredList = self.getLetteredList(len(rowsToUpdate))
			letCount = 0
			
			# for row in rowsToUpdate:
			for i in range(len(self.currentList)):
				currText = self.currentList[i]
				changedText = currText
				
				if i in rowsToUpdate:
					# base name block

					remB = self.ui.sb_removeBefore.value()
					if remB > 0: changedText = changedText[remB:]
					
					remA = self.ui.sb_removeAfter.value()
					if remA > 0: changedText = changedText[:(-remA)]

					base = self.ui.le_base.text().replace(" ", "")
					if base != "": changedText = base

					prefix = self.ui.le_prefix.text().replace(" ", "")
					if prefix != "": changedText = prefix + changedText

					sufix = self.ui.le_sufix.text().replace(" ", "")
					if sufix != "": changedText = changedText + sufix

					# find replace block

					findText = self.ui.le_find.text()
					if findText != "" and (findText in changedText):
						replaceText = self.ui.le_replace.text().replace(" ", "")
						changedText = changedText.replace(findText, replaceText)
					
					# numbered block

					if numbered and ("[num]" in changedText):
						changedText = changedText.replace("[num]", numberedList[numCount])
						numCount += 1
					else:
						changedText = changedText.replace("[num]", "")
					 
					# lettered block

					if lettered and ("[let]" in changedText) and (letCount < len(letteredList)):
						changedText = changedText.replace("[let]", letteredList[letCount])
						letCount += 1
					else:
						changedText = changedText.replace("[let]", "")
					
				# replace the current text
				if changedText != (self.ui.tw_namesList.item(i, 1).text()):
					self.ui.tw_namesList.item(i, 1).setText(changedText)

			self.enableUpdate()

	def getNumberedList(self, limit):
		numberedList = []

		starting = self.ui.sb_numberedStarting.value()
		digits = self.ui.sb_numberedDigits.value()
		increment = self.ui.sb_numberedIncrement.value()
		order = str(self.ui.cb_numberedOrder.currentText())

		for i in range(0, limit):
			index = i*increment + starting
			if order == "Descending": index = -i*increment + starting

			numberedList.append(str(index).zfill(digits))

		return numberedList

	def getLetteredList(self, limit):
		letteredList = []

		starting = self.ui.cb_letteredStarting.currentText()
		digits = self.ui.sb_letteredDigits.value()
		increment = self.ui.sb_letteredIncrement.value()
		order = str(self.ui.cb_letteredOrder.currentText())

		if starting != "":
			letteredPermutations = []
			letteredPermutations = self.getLetteredPermutation(letteredPermutations, deep=digits, lowerCase=False)
			starting = letteredPermutations.index(starting)
			
			if limit > len(letteredPermutations):
				addIterations = limit/len(letteredPermutations)
				defLetteredPermutations = letteredPermutations
				for i in range(0, addIterations):
					defLetteredPermutations += letteredPermutations

			for i in range(0, limit):
				index = i*increment + starting
				if order == "Descending": index = -i*increment + starting

				letteredList.append(letteredPermutations[index])

		return letteredList

	def letteredStartingUpdate(self):
		startingListItems = []

		numDigits = self.ui.sb_letteredDigits.value()
		startingListItems = self.getLetteredPermutation(startingListItems, deep=numDigits, lowerCase=False)
		
		self.ui.cb_letteredStarting.clear()
		self.ui.cb_letteredStarting.addItems(startingListItems)

	def getLetteredPermutation(self, originalList, deep=1, lowerCase=False):
		permutedList = []

		if deep > 0:
			letterSequence = "ABCDEFGHIJKLMNNOPQRSTUVWXYZ"
			if lowerCase: letterSequence = letterSequence.lower()

			if len(originalList) == 0:
				for c in letterSequence:
					permutedList.append(c)
			else:
				for item in originalList:
					for c in letterSequence:
						permutedList.append(item + c)

			if deep > 1:
				permutedList = self.getLetteredPermutation(permutedList, deep=(deep-1), lowerCase=lowerCase)

		return permutedList

def renamerRun():
	utils.closeTool('renamer')
	dTool = Renamer()

def renamerClose():
	utils.closeTool('renamer')
	
#######################################
# execution
if __name__ == "__main__": renamerRun()
