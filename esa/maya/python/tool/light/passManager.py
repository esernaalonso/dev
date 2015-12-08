#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys
import os

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.icons as icons
import esa.maya.python.lib.light.nodesets as nodesets
import esa.maya.python.lib.light.containers as containers

reload(utils)
reload(ui)
reload(icons)
reload(nodesets)
reload(containers)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class PassManager(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(PassManager, self).__init__(parent)

		self.setLayout(QtGui.QVBoxLayout())

		self.setObjectName('passManager')
		allowedAreas = ['right', 'left']
		self.dockCtrl = cmds.dockControl(label='Firefly Pass Manager', area='left', content=self.objectName(), allowedArea=allowedAreas )

		self.opened = True		
		self.initUI()

	def initUI(self):
		# layout
		self.setLayout(QtGui.QVBoxLayout())
		
		# add main widget
		self.mainWiget = PassManagerMainWiget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(0, 0, 0, 0)

		self.show()

	def closeEvent(self, event):
		self.opened = False
		cmds.deleteUI(self.dockCtrl)

class PassManagerMainWiget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(PassManagerMainWiget, self).__init__(parent)
		self.editing_selection = False

		self.scene_nodesets = nodesets.get_scene_nodesets()

		self.container_mediator = containers.ContainerTreesMediator()

		self.initUI()

	def initUI(self):
		# color vars
		self.nodeset_color = QtGui.QColor(25,25,25)

		# Icons
		self.layersNewIcon = icons.getIconByName("layers_16x16.png")
		self.layersNewSelectionIcon = icons.getIconByName("layersNew_16x16.png")
		self.layersDuplicateIcon = icons.getIconByName("layersDuplicate_16x16.png")
		self.layersDeleteIcon = icons.getIconByName("layersDelete_16x16.png")
		self.layersAddIcon = icons.getIconByName("layersAdd_16x16.png")
		self.layersRemoveIcon = icons.getIconByName("layersRemove_16x16.png")
		self.layersClearIcon = icons.getIconByName("layersClear_16x16.png")
		self.layersSelectObjectsIcon = icons.getIconByName("layersSelectObjects_16x16.png")
		self.layersSelectIcon = icons.getIconByName("layersSelect_16x16.png")
		self.layersLoadIcon = icons.getIconByName("layersLoad_16x16.png")
		self.objectIcon = icons.getIconByName("3Dobject_16x16.png")

		self.containerIcon = icons.getIconByName("container_16x16.png")
		self.passTreeIcon = icons.getIconByName("passTree_16x16.png")
		self.passGroupIcon = icons.getIconByName("passGroup_16x16.png")
		self.passIcon = icons.getIconByName("pass_16x16.png")
		self.overridesetIcon = icons.getIconByName("overrideset_16x16.png")
		self.overrideIcon = icons.getIconByName("override_16x16.png")
		self.lightsetIcon = icons.getIconByName("lightset_16x16.png")
		self.objectsetIcon = icons.getIconByName("objectset_16x16.png")
		self.lodsetIcon = icons.getIconByName("lodset_16x16.png")
		self.nodesetIcon = icons.getIconByName("nodeset_16x16.png")

		# Load UI file
		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)
		
		# Layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

		# Nodesets

		# Nodesets UI init
		self.nodesets_buttons_layout = self.ui.tab_all.widget(1).layout().children()[0]
		
		self.nodesets_buttons_layout.itemAt(0).widget().setIcon(self.layersNewIcon)
		self.nodesets_buttons_layout.itemAt(1).widget().setIcon(self.layersNewSelectionIcon)
		self.nodesets_buttons_layout.itemAt(2).widget().setIcon(self.layersDuplicateIcon)
		self.nodesets_buttons_layout.itemAt(3).widget().setIcon(self.layersDeleteIcon)

		self.nodesets_buttons_layout.itemAt(5).widget().setIcon(self.layersAddIcon)
		self.nodesets_buttons_layout.itemAt(6).widget().setIcon(self.layersRemoveIcon)
		self.nodesets_buttons_layout.itemAt(7).widget().setIcon(self.layersClearIcon)

		self.nodesets_buttons_layout.itemAt(9).widget().setIcon(self.layersSelectObjectsIcon)
		self.nodesets_buttons_layout.itemAt(10).widget().setIcon(self.layersSelectIcon)

		self.nodesets_buttons_layout.itemAt(12).widget().setIcon(self.layersLoadIcon)

		self.nodesets_tree = self.ui.tab_all.widget(1).layout().itemAt(0).widget()
		self.nodesets_tree.setColumnCount(1)
		self.nodesets_tree.setHeaderLabels(["Name"])
		# self.nodesets_tree.setColumnHidden(1, True)
		self.nodesets_tree.header().setResizeMode(0, QtGui.QHeaderView.Stretch)

		self.nodesets_name_edit = self.ui.tab_all.widget(1).layout().itemAt(2).widget()

		# Nodesets fill UI

		self.fill_nodesets_tree()

		# Nodesets UI signals

		self.nodesets_buttons_layout.itemAt(0).widget().clicked.connect(self.new_nodeset)
		self.nodesets_buttons_layout.itemAt(1).widget().clicked.connect(lambda: self.new_nodeset(selection=True))
		self.nodesets_buttons_layout.itemAt(2).widget().clicked.connect(self.duplicate_selected_nodesets)
		self.nodesets_buttons_layout.itemAt(3).widget().clicked.connect(self.remove_selected_nodesets)

		self.nodesets_buttons_layout.itemAt(5).widget().clicked.connect(self.add_selected_objects_to_nodesets)
		self.nodesets_buttons_layout.itemAt(6).widget().clicked.connect(self.remove_selected_objects_from_nodesets)
		self.nodesets_buttons_layout.itemAt(7).widget().clicked.connect(self.clear_nodesets)

		self.nodesets_buttons_layout.itemAt(9).widget().clicked.connect(self.select_nodests_objects)
		self.nodesets_buttons_layout.itemAt(10).widget().clicked.connect(self.select_objects_nodesets)

		self.nodesets_buttons_layout.itemAt(12).widget().clicked.connect(self.import_nodesets)

		self.nodesets_tree.itemSelectionChanged.connect(self.fix_nodesets_selection)
		self.nodesets_tree.itemSelectionChanged.connect(self.update_nodeset_name_edit)
		self.nodesets_tree.itemClicked.connect(self.select_nodesets_objects)

		self.nodesets_name_edit.returnPressed.connect(self.nodeset_rename)

		# Passes UI init
		# self.nodesets_buttons_layout = self.ui.tab_all.widget(1).layout().children()[0]
		
		self.tab_containers_spliter = self.ui.tab_all.widget(0).layout().itemAt(0).widget()
		self.tab_containers_spliter.setSizes([400,80])

		self.containers_buttons_layout = self.tab_containers_spliter.widget(0).layout().children()[0]
		
		self.containers_buttons_layout.itemAt(0).widget().setIcon(self.passTreeIcon)
		self.containers_buttons_layout.itemAt(1).widget().setIcon(self.passGroupIcon)
		self.containers_buttons_layout.itemAt(2).widget().setIcon(self.passIcon)

		self.containers_buttons_layout.itemAt(4).widget().setIcon(self.overrideIcon)
		self.containers_buttons_layout.itemAt(5).widget().setIcon(self.lightsetIcon)
		self.containers_buttons_layout.itemAt(6).widget().setIcon(self.objectsetIcon)
		self.containers_buttons_layout.itemAt(7).widget().setIcon(self.lodsetIcon)
		self.containers_buttons_layout.itemAt(8).widget().setIcon(self.nodesetIcon)

		self.containers_buttons_layout.itemAt(10).widget().setIcon(self.layersLoadIcon)

		self.containers_tree = self.tab_containers_spliter.widget(0).layout().itemAt(1).widget()
		self.containers_tree.setColumnCount(2)
		self.containers_tree.setHeaderLabels(["Name", "Info", "Type"])
		self.containers_tree.setColumnHidden(2, True)
		self.containers_tree.setColumnWidth(0,200)
		self.containers_tree.header().setResizeMode(1, QtGui.QHeaderView.Stretch)

		# self.containers_name_edit = self.ui.tab_all.widget(0).layout().itemAt(2).widget()

		# Passes fill Ui
		self.fill_containers_tree()

		# Passes UI signals

		self.containers_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.containers_tree.customContextMenuRequested.connect(self.pass_tree_menu)

		self.containers_buttons_layout.itemAt(0).widget().clicked.connect(lambda type="tree": self.new_container(type))
		self.containers_buttons_layout.itemAt(1).widget().clicked.connect(lambda type="group": self.new_container(type))
		self.containers_buttons_layout.itemAt(2).widget().clicked.connect(lambda type="pass": self.new_container(type))

		self.containers_buttons_layout.itemAt(4).widget().clicked.connect(lambda type="override": self.new_container(type))
		self.containers_buttons_layout.itemAt(5).widget().clicked.connect(lambda type="lightset": self.new_container(type))
		self.containers_buttons_layout.itemAt(6).widget().clicked.connect(lambda type="objectset": self.new_container(type))
		self.containers_buttons_layout.itemAt(7).widget().clicked.connect(lambda type="lodset": self.new_container(type))
		self.containers_buttons_layout.itemAt(8).widget().clicked.connect(lambda type="nodeset": self.new_container(type))

		self.containers_tree.itemSelectionChanged.connect(self.fix_containers_selection)
		# self.containers_tree.itemSelectionChanged.connect(self.update_container_name_edit)

		# self.containers_name_edit.returnPressed.connect(self.container_rename)

	def get_tree_item_level(self, item):
		level = -1

		while item:
			level += 1
			item = item.parent()

		return level

	def pass_tree_menu(self, position):
		menu = QtGui.QMenu(self.containers_tree)

		sel_items = self.containers_tree.selectedIndexes()
		
		if len(sel_items) > 0:
			index = sel_items[0]
			item = self.containers_tree.itemFromIndex(index)
			current_container = self.container_mediator.get_container_by_ui(item)
			
			for container_type in current_container.get_children_types_creatable():
				new_action = None
				new_action = QtGui.QAction(self)
				new_action.setText(("New " + container_type))
				new_action.triggered.connect(lambda type=container_type: self.new_container(type))
				menu.addAction(new_action)
		else:
			new_action = QtGui.QAction(self)
			new_action.setText("New tree")
			new_action.triggered.connect(lambda type="tree": self.new_container(type))
			menu.addAction(new_action)

		menu.exec_(self.containers_tree.viewport().mapToGlobal(position))

	def fix_containers_selection(self):
		if not self.editing_selection:
			self.editing_selection = True
			last_selected_level = 0

			sel_items = self.containers_tree.selectedItems()
			if len(sel_items) > 1:
				last_selected = sel_items[len(sel_items) - 1]
				last_selected_level = self.get_tree_item_level(last_selected)
				
				for sel_item in sel_items:
					level = self.get_tree_item_level(sel_item)
					if level != last_selected_level:
						sel_item.setSelected(False)

			self.select_nodesets_objects()

			self.editing_selection = False

	def get_tree_container_insert_index(self, container):
		insert_index = 0

		parent_container = container.get_parent()

		if parent_container:
			brtohers = parent_container.get_children()
			insert_index = len(brtohers)

			brothers_str = [str(ch) for ch in brtohers]
			insert_index = brothers_str.index(str(container))

		return insert_index

	def add_container_to_tree(self, container, parent=None):
		if not parent:
			item = QtGui.QTreeWidgetItem(self.containers_tree, [container.get_name(), container.get_info()])
		else:
			item = QtGui.QTreeWidgetItem(None, [container.get_name(), container.get_info(), container.get_type()])
			insert_index = self.get_tree_container_insert_index(container)
			parent.insertChild(insert_index, item)

		item.setSizeHint(0, QtCore.QSize(-1, 20))
		# item.setBackground(0, QtGui.QBrush(self.nodeset_color))

		if container.get_type() == "tree":
			item.setIcon(0, self.passTreeIcon)
			item.setExpanded(True)
		elif container.get_type() == "group":
			item.setIcon(0, self.passGroupIcon)
			item.setExpanded(True)
		elif container.get_type() == "pass":
			item.setIcon(0, self.passIcon)
			item.setExpanded(True)
		elif container.get_type() == "overrideset":
			item.setIcon(0, self.overridesetIcon)
			item.setExpanded(True)
		elif container.get_type() == "override":
			item.setIcon(0, self.overrideIcon)
			item.setExpanded(True)
		elif container.get_type() == "lightset":
			item.setIcon(0, self.lightsetIcon)
			item.setExpanded(True)
		elif container.get_type() == "objectset":
			item.setIcon(0, self.objectsetIcon)
			item.setExpanded(True)
		elif container.get_type() == "lodset":
			item.setIcon(0, self.lodsetIcon)
			item.setExpanded(True)
		elif container.get_type() == "nodeset":
			item.setIcon(0, self.nodesetIcon)
			item.setExpanded(True)
		else:
			item.setIcon(0, self.containerIcon)
			item.setExpanded(True)

		container.set_ui(item)

		if len(container.get_children()) > 0:
			for ch_container in container.get_children():
				self.add_container_to_tree(ch_container, parent=item)		

	def new_container(self, type):
		sel_items = self.containers_tree.selectedIndexes()

		if len(sel_items) > 0:
			items = []
			items_str = []

			for sel_item in sel_items:
				item = self.containers_tree.itemFromIndex(sel_item)
				if str(item) not in items_str:
					items.append(item)
					items_str.append(str(item))

			for item in items:
				parent_container = None
				parent_container = self.container_mediator.get_container_by_ui(item)

				new_container = self.container_mediator.create_container(type=type, parent=parent_container, new=True)
				if new_container:
					self.add_container_to_tree(new_container, parent=(parent_container.get_ui() if parent_container else None))
		else:
			new_container = self.container_mediator.create_container(type=type, new=True)
			if new_container:
				self.add_container_to_tree(new_container)

	def fill_containers_tree(self, refresh=False):
		trees = self.container_mediator.get_trees(refresh=refresh)
		
		for pass_tree in trees:
			self.add_container_to_tree(pass_tree)

	def nodeset_rename(self):
		if not self.editing_selection:
			sel_items = self.nodesets_tree.selectedItems()
			if len(sel_items) == 1:
				last_selected = sel_items[0]
				last_selected_level = self.get_tree_item_level(last_selected)

				if last_selected_level == 0:
					current_nodeset = nodesets.Nodeset(name=last_selected.text(0))
					index = self.get_nodeset_tree_index(current_nodeset)

					self.scene_nodesets[index].set_name(self.nodesets_name_edit.text())
					last_selected.setText(0, self.scene_nodesets[index].get_name())
					self.nodesets_name_edit.setText(self.scene_nodesets[index].get_name())
					self.nodesets_name_edit.setFocus()

	def update_nodeset_name_edit(self):
		if not self.editing_selection:
			sel_items = self.nodesets_tree.selectedItems()
			if len(sel_items) == 1:
				last_selected = sel_items[0]
				last_selected_level = self.get_tree_item_level(last_selected)

				if last_selected_level == 0:
					self.nodesets_name_edit.setText(last_selected.text(0))
					self.nodesets_name_edit.setFocus()
				else:
					self.nodesets_name_edit.clear()
			else:
				self.nodesets_name_edit.clear()

	def fix_nodesets_selection(self):
		if not self.editing_selection:
			self.editing_selection = True
			last_selected_level = 0

			sel_items = self.nodesets_tree.selectedItems()
			if len(sel_items) > 1:
				last_selected = sel_items[len(sel_items) - 1]
				last_selected_level = self.get_tree_item_level(last_selected)
				
				for sel_item in sel_items:
					level = self.get_tree_item_level(sel_item)
					if level != last_selected_level:
						sel_item.setSelected(False)

			self.select_nodesets_objects()

			self.editing_selection = False

	def add_nodeset_to_tree(self, nodeset):
		item = QtGui.QTreeWidgetItem(self.nodesets_tree, [nodeset.get_name()])
		item.setSizeHint(0, QtCore.QSize(-1, 20))
		item.setBackground(0, QtGui.QBrush(self.nodeset_color))
		item.setIcon(0, self.nodesetIcon)
		# item.setExpanded(True)

		nodeset_nodes = nodeset.get_nodes(fullPath=False)
		for nsn in nodeset_nodes:
			sub_item = QtGui.QTreeWidgetItem(item, [nsn])
			sub_item.setSizeHint(0, QtCore.QSize(-1, 20))
			sub_item.setIcon(0, self.objectIcon)

	def fill_nodesets_tree(self, reset=False):
		self.nodesets_tree.clear()
		
		if reset: self.scene_nodesets = nodesets.get_scene_nodesets()

		for ns in self.scene_nodesets:
			self.add_nodeset_to_tree(ns)

	def new_nodeset(self, name="new", selection=False):
		nodeset_new = nodesets.Nodeset(name=name, new=True, selection=selection)
		self.scene_nodesets.append(nodeset_new)
		self.add_nodeset_to_tree(nodeset_new)
		return nodeset_new

	def duplicate_nodeset(self, nodeset):
		new_name = nodeset.get_name()
		while new_name[len(new_name) - 1].isdigit(): new_name = new_name[:-1]

		nodeset_new = nodesets.Nodeset(name=new_name, new=True, nodes=nodeset.get_nodes())
		self.scene_nodesets.append(nodeset_new)
		self.add_nodeset_to_tree(nodeset_new)

	def duplicate_selected_nodesets(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					self.duplicate_nodeset(current_nodeset)

	def get_nodeset_tree_index(self, nodeset):
		index = -1
		for i in range(len(self.scene_nodesets)):
			if self.scene_nodesets[i].get_name() == nodeset.get_name():
				index = i
		return index

	def remove_nodeset(self, nodeset):
		index = self.get_nodeset_tree_index(nodeset)

		nodeset.remove()
		if index > -1:
			self.scene_nodesets.remove(self.scene_nodesets[index])
			self.nodesets_tree.takeTopLevelItem(index)

	def remove_selected_nodesets(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					self.remove_nodeset(current_nodeset)

	def add_selected_objects_to_nodeset(self, nodeset):
		curr_selection_long = cmds.ls(selection=True, long=True)
		curr_selection = cmds.ls(selection=True, long=False)
		curr_nodes_long = nodeset.get_nodes(fullPath=True)
		index = self.get_nodeset_tree_index(nodeset)
		if index > -1:
			item = self.nodesets_tree.topLevelItem(index)
			nodes_to_add = []
			for i in range(len(curr_selection)):
				if not curr_selection_long[i] in curr_nodes_long:
					nodes_to_add.append(curr_selection_long[i])

					sub_item = QtGui.QTreeWidgetItem(item, [curr_selection[i]])
					sub_item.setSizeHint(0, QtCore.QSize(-1, 20))
					sub_item.setIcon(0, self.objectIcon)

			if len(nodes_to_add) > 0:
				nodeset.add_nodes(nodes=nodes_to_add)

	def add_selected_objects_to_nodesets(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					self.add_selected_objects_to_nodeset(current_nodeset)

	def remove_selected_objects_from_nodeset(self, nodeset):
		curr_selection_long = cmds.ls(selection=True, long=True)
		curr_selection = cmds.ls(selection=True, long=False)
		curr_nodes_long = nodeset.get_nodes(fullPath=True)
		index = self.get_nodeset_tree_index(nodeset)

		if index > -1:
			item = self.nodesets_tree.topLevelItem(index)
			nodes_to_remove = []
			for i in range(len(curr_selection)):
				if curr_selection_long[i] in curr_nodes_long:
					nodes_to_remove.append(curr_selection_long[i])

					child_to_remove = None
					for j in range(item.childCount()):
						if item.child(j).text(0) == curr_selection[i]:
							child_to_remove = item.child(j)
					if child_to_remove:
						item.removeChild(child_to_remove)

			if len(nodes_to_remove) > 0:
				nodeset.remove_nodes(nodes=nodes_to_remove)

	def remove_selected_objects_from_nodesets(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			nodesets_to_remove_elements = []
			nodesets_to_remove_elements_names = []

			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					if sel_items[i].text(0) not in nodesets_to_remove_elements_names:
						nodesets_to_remove_elements_names.append(sel_items[i].text(0))
						nodesets_to_remove_elements.append(current_nodeset)
					# self.remove_selected_objects_from_nodeset(current_nodeset)
				elif level == 1:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].parent().text(0))
					if sel_items[i].parent().text(0) not in nodesets_to_remove_elements_names:
						nodesets_to_remove_elements_names.append(sel_items[i].parent().text(0))
						nodesets_to_remove_elements.append(current_nodeset)
					# self.remove_selected_objects_from_nodeset(current_nodeset)

			for ns in nodesets_to_remove_elements:
				self.remove_selected_objects_from_nodeset(ns)
			cmds.select(clear=True)

	def clear_nodeset(self, nodeset):
		index = self.get_nodeset_tree_index(nodeset)

		if index > -1:
			item = self.nodesets_tree.topLevelItem(index)
			
			children_to_remove = []
			for i in range(item.childCount()):
				children_to_remove.append(item.child(i))
			if len(children_to_remove) > 0:
				for ch in children_to_remove:
					item.removeChild(ch)

			nodeset.clear()

	def clear_nodesets(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					self.clear_nodeset(current_nodeset)

	def select_nodests_objects(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			nodes_to_select = []

			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					nodes_to_select.extend(current_nodeset.get_nodes(fullPath=True))

			if len(nodes_to_select) > 0:
				cmds.select(nodes_to_select)

	def select_objects_nodesets(self):
		self.nodesets_tree.clearSelection()
		curr_selection = cmds.ls(selection=True, long=True)
		for i in range(len(self.scene_nodesets)):
			nodes = self.scene_nodesets[i].get_nodes(fullPath=True)
			found = False
			for sel_node in curr_selection:
				if sel_node in nodes:
					item = self.nodesets_tree.topLevelItem(i)
					item.setSelected(True)
					break

	def select_nodesets_objects(self):
		sel_items = self.nodesets_tree.selectedItems()
		if len(sel_items) > 0:
			nodes_to_select = []

			for i in range(len(sel_items)):
				level = self.get_tree_item_level(sel_items[i])

				if level == 0:
					current_nodeset = nodesets.Nodeset(name=sel_items[i].text(0))
					nodes_to_select.append(current_nodeset.get_name(full=True))
				if level == 1:
					node_name = sel_items[i].text(0)
					parent_name = sel_items[i].parent().text(0)

					for ns in self.scene_nodesets:
						if parent_name == ns.get_name():
							nodes_names = ns.get_nodes(fullPath=False)
							nodes_names_full = ns.get_nodes(fullPath=True)

							if node_name in nodes_names:
								nodes_to_select.append(nodes_names_full[nodes_names.index(node_name)])

			if len(nodes_to_select) > 0:
				cmds.select(clear=True)
				cmds.select(nodes_to_select, noExpand=True)

	def import_nodesets(self):
		current_path = os.path.dirname(os.path.abspath(cmds.file(expandName=True, q=True)))
		current_file = os.path.basename(cmds.file(expandName=True, q=True))

		import_file = cmds.fileDialog2(ds=2, cap="Import Nodesets", dir=current_path, ff="*.ma", fm=1, okc="Import", cc="Cancel")

		if import_file:
			file_nodesets_names = nodesets.get_file_nodesets(import_file[0], mode="names")
			file_nodesets_nodes = nodesets.get_file_nodesets(import_file[0], mode="nodes")
			
			current_nodesets_names = [nodeset.get_name() for nodeset in self.scene_nodesets]

			conflicts = False
			for nsn in file_nodesets_names:
				if nsn in current_nodesets_names:
					conflicts = True
					break

			answer = 'Load'
			if conflicts:
				answer = cmds.confirmDialog( title='Conflicts', message='Some of the nodesets you are about to import are already in scene. What do you want to do?', button=['Merge','Replace', 'Rename', 'Ignore', 'Cancel'], defaultButton='Merge', cancelButton='Cancel', dismissString='Cancel', icon='warning')

			if answer != 'Cancel':
				for i in range(len(file_nodesets_names)):
					name = file_nodesets_names[i]
					nodes = file_nodesets_nodes[i]

					if name in current_nodesets_names:
						if answer != 'Ignore':
							index = current_nodesets_names.index(name)
							if answer == 'Merge' or answer == 'Replace':
								nodeset_current = self.scene_nodesets[index]
								if answer == 'Replace':
									self.clear_nodeset(nodeset_current)
								cmds.select(nodes)
								self.add_selected_objects_to_nodeset(nodeset_current)
							elif answer == 'Rename':
								nodeset_new = self.new_nodeset(name=name)
								current_nodesets_names.append(nodeset_new.get_name())
								cmds.select(nodes)
								self.add_selected_objects_to_nodeset(nodeset_new)
					else:
						nodeset_new = self.new_nodeset(name=name)
						current_nodesets_names.append(nodeset_new.get_name())
						cmds.select(nodes)
						self.add_selected_objects_to_nodeset(nodeset_new)


def passManagerRun():
	utils.closeTool('passManager', dock=True)
	dTool = PassManager()

def passManagerClose():
	utils.closeTool('passManager', dock=True)

#######################################
# execution
if __name__ == "__main__": passManagerRun()