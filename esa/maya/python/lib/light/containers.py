#######################################
# imports

import maya.cmds as cmds

import esa.maya.python.lib.shader as shader

reload(shader)

#######################################
# attributes

#######################################
# definitions

#######################################
# classes

class Container(object):
	def __init__(self, name=None, type="generic", parent=None, new=False, virtual=False, factory=None, ui=None):
		self.prefix = "container"
		self.default_names = ["new001", "tree001", "group001", "pass001", "overrides", "override001", "lightset001", "objectset001", "lodset001", "nodeset001"]
		self.types = ["generic", "tree", "group", "pass", "overrideset", "override", "lightset", "objectset", "lodset", "nodeset"]
		self.children_types = ["generic", "tree", "group", "pass", "overrideset", "override", "lightset", "objectset", "lodset", "nodeset"]
		self.children_types_creatable = ["generic", "tree", "group", "pass", "overrideset", "override", "lightset", "objectset", "lodset", "nodeset"]
		self.types_sort = ["overrideset", "generic", "tree", "group", "pass", "override", "lightset", "objectset", "lodset", "nodeset"]
		self.types_colors = {"generic":[0.5,0.5,0.5], "tree":[0.128,0.585,0.949], "group":[0.128,0.585,0.949], "pass":[0.128,0.585,0.949], "overrideset":[0.910,0.117,0.386], "override":[0.910,0.117,0.386], "lightset":[1.0,0.761,0.230], "objectset":[0.296,0.683,0.312], "lodset":[0.0,0.585,0.531], "nodeset":[0.896,0.209,0.015]}

		self.type = type if type in self.types else "generic"
		self.name = name if name else self.default_names[self.types.index(self.type)]
		self.parent = parent if parent != self else None
		self.children = []
		self.virtual = virtual
		self.factory = factory
		self.ui = ui

		exists = len(cmds.ls(self.get_compound_name())) > 0

		if (exists and not new) or virtual:
			self.container_object = self.get_compound_name()

			if self.parent:
				self.parent.add_child(self)
		else:
			self.container_object = self.create_container_object()

			cmds.addAttr(self.container_object, sn="cname", ln="container_name", nn="Container Name", ci=True, dt="string")
			cmds.addAttr(self.container_object, sn="ctype", ln="container_type", nn="Container Type", ci=True, dt="string")
			
			cmds.setAttr((self.container_object + ".cname"), self.name, type="string")
			cmds.setAttr((self.container_object + ".ctype"), self.type, type="string")

			if self.parent:
				self.container_object = cmds.parent(self.get_container_object(), parent.get_container_object(fullPath=True))[0].split("|")[-1:][0]
				self.update_name()
				self.parent.add_child(self)

		if not self.virtual and len(self.children)==0:
			children_objects = self.get_children_objects()
			if len(children_objects) > 0:
				for ch in children_objects:
					child_container = self.factory.create_container_from_scene_object(ch, parent=self, new=False, virtual=virtual)
	def get_compound_prefix(self):
		return (self.prefix + "_" + self.type)

	def get_compound_name(self):
		return (self.get_compound_prefix() + "_" + self.name)

	def update_name(self):
		self.name = self.get_container_object().replace((self.get_compound_prefix() + "_"), "")

	def update_color(self):
		cmds.setAttr(self.container_object + ".useOutlinerColor", True)
		cmds.setAttr(self.container_object + ".outlinerColor", self.types_colors[self.type][0], self.types_colors[self.type][1], self.types_colors[self.type][2], type="double3")

		cmds.setAttr(self.container_object + ".overrideRGBColors", 1)
		cmds.setAttr(self.container_object + ".overrideColorRGB", self.types_colors[self.type][0], self.types_colors[self.type][1], self.types_colors[self.type][2], type="double3")
		cmds.setAttr(self.container_object + ".overrideEnabled", True)

	def create_container_object(self, size=0.1):
		self.container_object = cmds.spaceLocator(p=(0, 0, 0))[0]
		self.container_object = cmds.rename(self.container_object, self.get_compound_name())
		self.name = self.container_object.replace((self.get_compound_prefix() + "_"), "").replace("|","")

		self.update_color()
		return self.container_object

	def get_container_object(self, fullPath=False):
		if fullPath:
			if self.get_parent():
				parent_path = self.get_parent().get_container_object(fullPath=True)
				return (parent_path + "|" + self.container_object)
			else:
				return self.container_object
		else:
			return self.container_object

	def get_name(self):
		return self.name

	def get_info(self):
		return (self.type + " container")

	def get_type(self):
		return self.type

	def get_parent(self):
		return self.parent

	def get_children_objects(self):
		relatives_shapes = cmds.listRelatives(self.get_container_object(fullPath=True), shapes=True)
		children_objects = cmds.listRelatives(self.get_container_object(fullPath=True), children=True)
		children_objects = [ch for ch in children_objects if ch not in relatives_shapes]

		children_objects_sorted = []

		for type in self.types_sort:
			for ch in children_objects:
				if type == ch.split("_")[1]:
					children_objects_sorted.append(ch)

		return children_objects_sorted

	def get_children(self):
		children_sorted = []

		for type in self.types_sort:
			for ch in self.children:
				if ch.get_type() == type:
					children_sorted.append(ch)

		return children_sorted

	def get_children_types(self):
		return self.children_types

	def get_children_types_creatable(self):
		return self.children_types_creatable

	def get_ui(self):
		return self.ui

	def set_ui(self, ui):
		self.ui = ui

	def set_parent(self, parent):
		if parent != self:
			self.parent = parent

	def new_child(self, name=None, type="generic", virtual=False):
		new_child = self.factory.create_container(name=name, type=type, parent=self, new=True, virtual=virtual)
		return new_child

	def add_child(self, child_container):
		child_container.set_parent(self)
		if (child_container not in self.children) and (child_container != self):
			self.children.append(child_container)

class ContainerTree(Container):
	def __init__(self, name=None, type="tree", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerTree, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["overrideset", "group"]
		self.children_types_creatable = ["group"]

		if len(self.get_children()) > 0:
			overrideset_container = [ch for ch in self.children if ch.get_type() == "overrideset"][0]
			if not overrideset_container: self.new_child(type="overrideset")
		else:
			self.new_child(type="overrideset")

	# def get_info(self):
		# TO DO return number of pass groups and passes

class ContainerGroup(Container):
	def __init__(self, name=None, type="group", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerGroup, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["overrideset", "pass"]
		self.children_types_creatable = ["pass"]

		if len(self.get_children()) > 0:
			overrideset_container = [ch for ch in self.children if ch.get_type() == "overrideset"][0]
			if not overrideset_container: self.new_child(type="overrideset")
		else:
			self.new_child(type="overrideset")

class ContainerPass(Container):
	def __init__(self, name=None, type="pass", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerPass, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["overrideset", "lightset", "objectset", "lodset"]
		self.children_types_creatable = ["lightset", "objectset", "lodset"]

		if len(self.get_children()) > 0:
			overrideset_container = [ch for ch in self.children if ch.get_type() == "overrideset"][0]
			if not overrideset_container: self.new_child(type="overrideset")
		else:
			self.new_child(type="overrideset")

class ContainerOverrideset(Container):
	def __init__(self, name=None, type="overrideset", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerOverrideset, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["override"]
		self.children_types_creatable = self.children_types

class ContainerOverride(Container):
	def __init__(self, name=None, type="override", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerOverride, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = []
		self.children_types_creatable = self.children_types

class ContainerLightset(Container):
	def __init__(self, name=None, type="lightset", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerLightset, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = []
		self.children_types_creatable = self.children_types

class ContainerObjectset(Container):
	def __init__(self, name=None, type="objectset", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerObjectset, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["overrideset", "nodeset"]
		self.children_types_creatable = ["nodeset"]

		if len(self.get_children()) > 0:
			overrideset_container = [ch for ch in self.children if ch.get_type() == "overrideset"][0]
			if not overrideset_container: self.new_child(type="overrideset")
		else:
			self.new_child(type="overrideset")

class ContainerLodset(Container):
	def __init__(self, name=None, type="lodset", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerLodset, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = ["overrideset", "nodeset"]
		self.children_types_creatable = ["nodeset"]

		if len(self.get_children()) > 0:
			overrideset_container = [ch for ch in self.children if ch.get_type() == "overrideset"][0]
			if not overrideset_container: self.new_child(type="overrideset")
		else:
			self.new_child(type="overrideset")

class ContainerNodeset(Container):
	def __init__(self, name=None, type="nodeset", parent=None, new=False, virtual=False, factory=None, ui=None):
		super(ContainerNodeset, self).__init__(name=name, type=type, parent=parent, new=new, virtual=virtual, factory=factory, ui=ui)

		self.children_types = []
		self.children_types_creatable = self.children_types

class ContainerFactory(Container):
	def __init__(self, name="factory"):
		super(ContainerFactory, self).__init__(name=name, type="generic", virtual=True)
		self.container_types = [Container, ContainerTree, ContainerGroup, ContainerPass, ContainerOverrideset, ContainerOverride, ContainerLightset, ContainerObjectset, ContainerLodset, ContainerNodeset]
		
	def get_scene_container_objects(self):
		scene_container_objects = []
		for type in self.types:
			scene_container_objects += cmds.ls((self.prefix + "_" + type + "_*"), transforms=True)
		return scene_container_objects

	def get_scene_container_root_objects(self, root_type=None):
		scene_container_root_objects = []

		scene_container_objects = self.get_scene_container_objects()
		for sco in scene_container_objects:
			parent = cmds.listRelatives(sco, parent=True)
			if not parent:
				if root_type:
					if (self.prefix + "_" + root_type + "_") in sco:
						scene_container_root_objects.append(sco)
				else:
					scene_container_root_objects.append(sco)
		return scene_container_root_objects

	def create_container(self, name=None, type="generic", parent=None, new=False, virtual=False, ui=None):
		new_container = None
		if type not in self.types: type = "generic"
		
		if not parent or (type in parent.children_types):
			index = self.types.index(type)
			new_container = self.container_types[index](name=name, type=type, parent=parent, new=new, virtual=virtual, factory=self, ui=ui)
		return new_container

	def create_container_from_scene_object(self, scene_object, parent=None, new=False, virtual=False, ui=None):
		ctype = scene_object.split("_")[1]
		cname = scene_object.replace((self.prefix + "_" + ctype + "_"), "")

		new_container = self.create_container(name=cname, type=ctype, parent=parent, new=new, virtual=virtual, ui=ui)
		return new_container

	def get_container_trees(self, root_type=None):
		container_trees = []
		scene_container_root_objects = self.get_scene_container_root_objects(root_type=root_type)

		for scro in scene_container_root_objects:
			container_trees.append(self.create_container_from_scene_object(scro))

		return container_trees


class ContainerTreesMediator(ContainerFactory):
	def __init__(self):
		super(ContainerTreesMediator, self).__init__(name="mediator")
		self.trees = []
		self.refresh()

	def refresh(self):
		self.trees = self.get_container_trees(root_type="tree")

	def get_trees(self, refresh=False):
		if refresh: self.refresh()
		return self.trees

	def create_container(self, name=None, type="generic", parent=None, new=False, virtual=False, ui=None):
		new_container = super(ContainerTreesMediator, self).create_container(name=name, type=type, parent=parent, new=new, virtual=virtual, ui=ui)

		if type == "tree":
			self.trees.append(new_container)
		return new_container

	def get_container_by_ui(self, ui_item, search_trees=None):
		requested_container = None

		if not search_trees:
			search_trees = self.trees

		for tree in search_trees:
			if requested_container:
				break
			else:
				if str(ui_item) == str(tree.get_ui()):
					requested_container = tree
				else:
					if len(tree.get_children()) > 0:
						requested_container = self.get_container_by_ui(ui_item, search_trees=tree.get_children())

		return requested_container


#######################################
# execution

if __name__ == "__main__":
	# for type in pass_container_types:
		# create_container_object("new", type=type)

	# ctnr = Container(type="generic")
	# for type in ctnr.types:
	# 	Container(type=type)

	# ctnr2 = Container(name="resource", type="generic", new=True, virtual=True)
	# # print ctnr2.container_object

	# container_factory = ContainerFactory()
	# pass_tree = container_factory.create_container(type="tree")
	# # print container_factory.get_scene_container_objects()

	# container_mediator = ContainerTreesMediator()
	# pass_tree = container_mediator.create_container(type="tree")
	# # print container_mediator.get_scene_container_root_objects()
	# for ch in container_mediator.trees[0].children: # print ch.get_name()

	container_mediator = ContainerTreesMediator()
	# print len(container_mediator.trees)

	# print container_mediator.trees[0].get_name()
	# print container_mediator.trees[0].get_parent()
	# print container_mediator.trees[0].get_children()

	# print container_mediator.trees[0].get_children()[0].get_name()
	# print container_mediator.trees[0].get_children()[0].get_parent()
	# print container_mediator.trees[0].get_children()[0].get_children()

	# # print container_mediator.trees[0].get_children()[0].get_children()[0].get_name()
	# # print container_mediator.trees[0].get_children()[0].get_children()[0].get_parent()
	# # print container_mediator.trees[0].get_children()[0].get_children()[0].get_children()

	pass