#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys
import os
import ntpath
import importlib
import itertools

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.main as main
import esa.maya.python.lib.listUtils as listUtils
import esa.maya.python.lib.icons as icons
import esa.maya.python.lib.pack as pack

reload(utils)
reload(ui)
reload(main)
reload(listUtils)
reload(icons)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class ToolManager(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(ToolManager, self).__init__(parent)
		
		self.setObjectName("toolManager")

		self.initUI()
		
		allowedAreas = ['right', 'left']
		self.dockCtrl = cmds.dockControl(label='Tool Manager', area='right', content=self.objectName(), allowedArea=allowedAreas )

		self.opened = True

	# init de UI
	def initUI(self):		
		# layout
		self.setLayout(QtGui.QVBoxLayout())
		
		# add main widget
		self.mainWiget = ToolList()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(0, 0, 0, 0)

		self.show()

	# close event
	def closeEvent(self, event):
		self.opened = False
		cmds.deleteUI(self.dockCtrl)

class ToolList(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ToolList, self).__init__(parent)
				
		self.initUI()

	# init de UI
	def initUI(self):
		# color vars
		self.foregroundColor = QtGui.QColor(200,200,200)
		self.categoryColor = QtGui.QColor(75,75,75)
		self.openStateColor = QtGui.QColor(0,255,100)
		self.closeStateColor = QtGui.QColor(255,160,0)
		self.executeStateColor = QtGui.QColor(0,170,255)

		self.categoryIcon = icons.getIconByName("folder_16x16.png")
		self.toolIcon = icons.getIconByName("tool_16x16.png")
		self.toolOpenIcon = icons.getIconByName("tool-open_16x16.png")
		self.scriptIcon = icons.getIconByName("gear_16x16.png")

		# load UI file
		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)
		
		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

		# fNewFont = QtGui.QFont("Courier",8,QtGui.QFont.Normal)
		# fNewFont.setLetterSpacing(QtGui.QFont.PercentageSpacing,0.0)

		# tree config
		self.ui.tr_toolsTree.setColumnCount(3)
		self.ui.tr_toolsTree.setHeaderLabels(["Name", "State", "h_FileName", "h_type"])
		self.ui.tr_toolsTree.setColumnHidden(2, True)
		self.ui.tr_toolsTree.setColumnHidden(3, True)
		self.ui.tr_toolsTree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)
		self.ui.tr_toolsTree.header().setResizeMode(1, QtGui.QHeaderView.Fixed)
		self.ui.tr_toolsTree.setColumnWidth(1,73)
		# self.ui.tr_toolsTree.setTextAlignment(1, QtCore.Qt.AlignVCenter)

		# tree fill
		self.fillTree()

		# add signals to the ui elements
		self.ui.rb_filterAnd.clicked.connect(self.refresh)
		self.ui.rb_filterOr.clicked.connect(self.refresh)
		self.ui.le_filter.editingFinished.connect(self.refresh)
		self.ui.cb_showTools.clicked.connect(self.refresh)
		self.ui.cb_showScripts.clicked.connect(self.refresh)
		self.ui.pb_refresh.clicked.connect(self.refresh)
		self.ui.pb_closeAll.clicked.connect(self.closeAll)
		self.ui.tr_toolsTree.itemClicked.connect(self.clickTreeItemExecution)
		self.ui.tr_toolsTree.itemDoubleClicked.connect(self.doubleClickTreeItemExecution)

		self.ui.tr_toolsTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.tr_toolsTree.customContextMenuRequested.connect(self.treeMenu)

	def treeMenu(self, position):
		selItems = self.ui.tr_toolsTree.selectedIndexes()
		
		if len(selItems) > 0:
			level = 0

			index = selItems[0]
			item = self.ui.tr_toolsTree.itemFromIndex(index)
			isleaf = item.childCount() == 0

			while index.parent().isValid():
				index = index.parent()
				level += 1

			menu = QtGui.QMenu(self.ui.tr_toolsTree)

			if isleaf:
				if item.text(3) == "tool" or item.text(3) == "script":
					packToolAction = QtGui.QAction(self)
					packToolAction.setText("pack tool")
					packToolAction.triggered.connect(self.packTool)
					menu.addAction(packToolAction)

					menu.exec_(self.ui.tr_toolsTree.viewport().mapToGlobal(position))

	# return the list of elements filtered by the interface choose
	def filterListElements(self, originList):
		filteredList = originList

		# removes this tool from the list to prevent self closing
		if len(filteredList) > 0:
			for i in range((len(filteredList) - 1), -1, -1):
				if "toolManager.py" in filteredList[i]:
					filteredList.remove(filteredList[i])

		# gets the filters to be used
		filters = self.ui.le_filter.text().split(" ")
		
		# applies the filters using AND or OR operation depending on the UI choose
		if self.ui.rb_filterAnd.isChecked():
			for fltr in filters:
				for i in range((len(filteredList) - 1), -1, -1):
					if not fltr.lower() in filteredList[i].lower():
						filteredList.remove(filteredList[i])
		elif self.ui.rb_filterOr.isChecked():
			for i in range((len(filteredList) - 1), -1, -1):
				bFound = False
				for fltr in filters:
					if fltr.lower() in filteredList[i].lower():
						bFound = True
				if not bFound:
					filteredList.remove(filteredList[i])

		return filteredList

	# get the elements that has to be shown in the list
	def getListElements(self):
		lTools = main.getTools()
		lScripts = main.getScripts()

		lAllElements = []

		# get all tools and scripts
		if (self.ui.cb_showTools.checkState()): lAllElements.extend(lTools)
		if (self.ui.cb_showScripts.checkState()): lAllElements.extend(lScripts)

		# filters all elements by UI choose
		self.filterListElements(lAllElements)
		
		return lAllElements
	
	# fill the list with tools and scripts
	def fillTree(self):
		# clear the tree
		self.ui.tr_toolsTree.clear()

		# get the elements for the list
		lElements = self.getListElements()
		
		# iterate the elements adding them to the list
		currentCategoriesItems = []
		currentCategories = []
		currentParent = self.ui.tr_toolsTree
		currentParentName = ""
		for i in range(len(lElements)):
			# get the type and name
			sElementName = os.path.splitext(ntpath.basename(lElements[i]))[0]
			sType = main.getPyFileType(lElements[i])

			# state options
			if sType == "tool":
				bOpened = utils.isToolOpened(sElementName)

				if bOpened:
					sState = "Close"
					cStateColor = self.closeStateColor
				else:
					sState = "Open"
					cStateColor = self.openStateColor
			elif sType == "script":
				sState = "Execute"
				cStateColor = self.executeStateColor

			# list the tool/script categories
			lCategories = main.getPyFileCategoryTree(lElements[i])

			if set(currentCategories) != set(lCategories):
				if len(currentCategories) == 0:
					currentParent = self.ui.tr_toolsTree
					currentParentName = ""
				elif listUtils.isSublist(currentCategories, lCategories) and (currentCategories[0] == lCategories[0]):
					lCategories = (list(set(lCategories) - set(currentCategories)))
				elif listUtils.isSublist(lCategories, currentCategories) and (currentCategories[0] == lCategories[0]):
					extra = (list(set(currentCategories) - set(lCategories)))
					currentCategories = currentCategories[:-len(extra)]
					currentCategoriesItems = currentCategoriesItems[:-len(extra)]
					currentParent = currentCategoriesItems[len(currentCategoriesItems)-1]
					currentParentName = currentCategories[len(currentCategories)-1]
				else:
					tmpCategories = lCategories
					while not listUtils.isSublist(tmpCategories, currentCategories) and len(tmpCategories) > 0:
						tmpCategories = tmpCategories[:-1]

					if len(tmpCategories) > 0:
						extra = (list(set(currentCategories) - set(tmpCategories)))
						currentCategories = currentCategories[:-len(extra)]
						currentCategoriesItems = currentCategoriesItems[:-len(extra)]
						currentParent = currentCategoriesItems[len(currentCategoriesItems)-1]
						currentParentName = currentCategories[len(currentCategories)-1]
						lCategories = (list(set(lCategories) - set(tmpCategories)))
					else:
						currentParent = self.ui.tr_toolsTree
						currentParentName = ""
						currentCategoriesItems = []
						currentCategories = []

				for cat in lCategories:
					item = QtGui.QTreeWidgetItem(currentParent,[cat])
					item.setExpanded(True)
					item.setForeground(0, QtGui.QBrush(self.foregroundColor))
					item.setForeground(1, QtGui.QBrush(self.foregroundColor))
					item.setBackground(0, QtGui.QBrush(self.categoryColor))
					item.setBackground(1, QtGui.QBrush(self.categoryColor))
					item.setIcon(0, self.categoryIcon)
					currentParent = item
					currentParentName = cat
					currentCategories.append(cat)
					currentCategoriesItems.append(item)
			
			item = QtGui.QTreeWidgetItem(currentParent, [sElementName, sState, lElements[i], sType])
			# item.setBackground(1, QtGui.QBrush(cStateColor))
			item.setForeground(0, QtGui.QBrush(self.foregroundColor))
			item.setForeground(1, QtGui.QBrush(self.foregroundColor))
			item.setSizeHint(1, QtCore.QSize(-1, 20))
			item.setTextAlignment(1, QtCore.Qt.AlignCenter)
			if sType == "tool":
				item.setIcon(1, self.toolIcon)
			else:				
				item.setIcon(1, self.scriptIcon)

	# refresh the list interface
	def refresh(self):
		self.fillTree()

	# return all tree leaf items
	def getTreeLeafItems(self, topItem=None):
		leafItems = []

		if not topItem:
			for i in range(self.ui.tr_toolsTree.topLevelItemCount()):
				item = self.ui.tr_toolsTree.topLevelItem(i)

				if item.childCount() == 0:
					leafItems.append(item)
				else:
					for j in range(item.childCount()):
						leafItems += self.getTreeLeafItems(topItem=item.child(j))
		else:
			if topItem.childCount() == 0:
				leafItems.append(topItem)
			else:
				for j in range(topItem.childCount()):
					leafItems += self.getTreeLeafItems(topItem=topItem.child(j))

		return leafItems

	# close all opened tools
	def closeAll(self):
		leafItems = self.getTreeLeafItems()
		
		for i in range(len(leafItems)):
			sToolFileName = leafItems[i].text(2)

			sToolName = leafItems[i].text(0)
			sType = main.getPyFileType(sToolFileName)
			
			if sType == "tool":
				bOpened = utils.isToolOpened(sToolName)
				if bOpened:
					isDockable = utils.isToolDockable(sToolName)
					utils.closeTool(sToolName, dock=isDockable)
				else:
					utils.closeTool(sToolName)

				# leafItems[i].setBackground(1, QtGui.QBrush(self.openStateColor))
				leafItems[i].setIcon(1, self.toolIcon)
				leafItems[i].setForeground(1, QtGui.QBrush(self.foregroundColor))
				leafItems[i].setText(1, "Open")
					
	def doubleClickTreeItemExecution(self, item, column):
		if column == 0:
			self.treeItemExecution(item, column)

	def clickTreeItemExecution(self, item, column):
		if column == 1:
			self.treeItemExecution(item, column)

	# open/close/execute the selected tool or script
	def treeItemExecution(self, item, column):
		if item.childCount() == 0:
			sToolName = item.text(0)
			sToolFileName = item.text(2)
		
			sType = main.getPyFileType(sToolFileName)
			# oModule = utils.importModule(sToolName)
			importStatement = main.getPyFileFullImportName(sToolFileName)
			print sToolFileName
			oModule = importlib.import_module(importStatement)
				
			# If the module can be run or closed
			if sType == "tool":
				bOpened = utils.isToolOpened(sToolName)

				# run or close the tool
				if bOpened:
					isDockable = utils.isToolDockable(sToolName)
					utils.closeTool(sToolName, dock=isDockable)
				else: utils.openTool(sToolName, module=oModule)

				# if the module is a tool the Open/Close label must be updated
				bOpened = utils.isToolOpened(sToolName)
				
				if bOpened:
					# item.setBackground(1, QtGui.QBrush(self.closeStateColor))
					item.setForeground(1, QtGui.QBrush(self.closeStateColor))
					item.setIcon(1, self.toolOpenIcon)
					item.setText(1, "Close")
				else:
					# item.setBackground(1, QtGui.QBrush(self.openStateColor))
					item.setForeground(1, QtGui.QBrush(self.foregroundColor))
					item.setIcon(1, self.toolIcon)
					item.setText(1, "Open")

			elif sType == "script":
				utils.executeScript(sToolName, module=oModule)

	def packTool(self):
		selItems = self.ui.tr_toolsTree.selectedIndexes()
		index = selItems[0]
		item = self.ui.tr_toolsTree.itemFromIndex(index)

		sToolName = item.text(0)
		pyFile = item.text(2)
		packFolder = pack.getPackFolder(pyFile)

		confirmMessage = 'You are about to pack "' + sToolName + '" and all its dependencies to "' + packFolder + '.\n\nThe packed tool/script will be standalone and you can locate it where you want. I usually move it to the local "maya/version/prefs/scripts" folder for the user. Then inside maya (no need to restart) I use this commands to open the tool/script:\n\nimport ' + sToolName + '.' + sToolName + ' as ' + sToolName + '\n' + sToolName + '.' + sToolName + 'Run()'
		answer = cmds.confirmDialog(t="Alert", message=confirmMessage, button=["Cancel", "Yes"], icon="warning")
		
		if answer == "Yes":
			pack.packPyFile(item.text(2), removePrevious=True)

			confirmMessage = '"' + sToolName + '" packed to "' + packFolder + '"'
			cmds.confirmDialog(t="Success Packing", message=confirmMessage, button=["OK"])

def toolManagerRun():
	utils.closeTool("toolManager", dock=True)
	dTool = ToolManager()

def toolManagerClose():
	utils.closeTool("toolManager", dock=True)

#######################################
# execution

if __name__ == "__main__": toolManagerRun()