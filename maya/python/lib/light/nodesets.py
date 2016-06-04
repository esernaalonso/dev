#######################################
# imports

import maya.cmds as cmds

import re
import os

#######################################
# attributes

nodeset_prefix = "nodeset"
nodeset_main_name = "main_container"

#######################################
# functionality

class Nodeset(object):
	def __init__(self, name="new", selection=False, nodes=[], flatten=True, new=False):
		super(Nodeset, self).__init__()

		self.name = (nodeset_prefix + "_" + name)
		self.uiObject = None

		try:
			proof_of_life = cmds.sets(self.name, q=True)
			proof_of_life = True
		except:
			proof_of_life = False
		
		if not proof_of_life or new:
			self.name = cmds.sets(name=self.name, text="gCharacterSet", empty=True)

			cmds.addAttr(self.name, sn="nodesetName", ln="nodesetName", ci=True, dt="string")
			cmds.addAttr(self.name, sn="nodesetNodes", ln="nodesetNodes", ci=True, dt="string")

			cmds.setAttr((self.name + ".nodesetName"), self.name, type="string")

			if selection:
				cmds.sets(cmds.ls(selection=True, long=True), include=self.name, e=True)
				if flatten: cmds.sets(flatten=self.name, e=True)

			if len(nodes) > 0:
				cmds.sets(nodes, include=self.name, e=True)
				if flatten: cmds.sets(flatten=self.name, e=True)

			self.main_nodeset = None
			if name != nodeset_main_name:
				self.main_nodeset = Nodeset(name=nodeset_main_name)
				self.main_nodeset.add_nodes(nodes=[self.name], flatten=False)

				cmds.setAttr((self.name + ".nodesetNodes"), str(self.get_nodes(fullPath=True)), type="string")

	def get_nodes(self, fullPath=True):
		sel_backup = cmds.ls(selection=True, long=True)
		cmds.select(self.name)
		nodeset_nodes = cmds.ls(selection=True, long=fullPath)
		cmds.select(sel_backup)
		return nodeset_nodes

	def set_nodes(self, selection=False, nodes=[], flatten=True):
		self.clear()
		self.add_nodes(self, selection=selection, nodes=nodes, flatten=flatten)
		
		if nodeset_main_name not in self.name:
			cmds.setAttr((self.name + ".nodesetNodes"), str(self.get_nodes(fullPath=True)), type="string")

	def add_nodes(self, selection=False, nodes=[], flatten=True):
		if selection:
			cmds.sets(cmds.ls(selection=True, long=True), include=self.name, e=True)
			if flatten: cmds.sets(flatten=self.name, e=True)

		if len(nodes) > 0:
			cmds.sets(nodes, include=self.name, e=True)
			if flatten: cmds.sets(flatten=self.name, e=True)

		if nodeset_main_name not in self.name:
			cmds.setAttr((self.name + ".nodesetNodes"), str(self.get_nodes(fullPath=True)), type="string")

	def remove_nodes(self, selection=False, nodes=[]):
		if selection:
			cmds.sets(cmds.ls(selection=True, long=True), remove=self.name, e=True)

		if len(nodes) > 0:
			cmds.sets(nodes, remove=self.name, e=True)

		if nodeset_main_name not in self.name:
			cmds.setAttr((self.name + ".nodesetNodes"), str(self.get_nodes(fullPath=True)), type="string")

	def get_name(self, full=False):
		if not full:
			return (self.name.replace((nodeset_prefix + "_"), ""))
		else:
			return self.name 

	def set_name(self, new_name=None):
		if new_name:
			self.name = cmds.rename(self.name, (nodeset_prefix + "_" + new_name))
			cmds.setAttr((self.name + ".nodesetName"), self.name, type="string")
			# self.name = (nodeset_prefix + "_" + new_name)

	def clear(self):
		self.remove_nodes(nodes=self.get_nodes(fullPath=True))
		
		if nodeset_main_name not in self.name:
			cmds.setAttr((self.name + ".nodesetNodes"), str(self.get_nodes(fullPath=True)), type="string")

	def remove(self):
		cmds.delete(self.name)

def get_scene_nodesets():
	scene_nodesets = []

	nodesets_nodes = cmds.ls((nodeset_prefix + "_*"), long=True)
	if nodesets_nodes and len(nodesets_nodes) > 0:
		if (nodeset_prefix + "_" + nodeset_main_name) in nodesets_nodes:
			nodesets_nodes.remove(nodeset_prefix + "_" + nodeset_main_name)

		if len(nodesets_nodes) > 0:
			for nsn in nodesets_nodes:
				scene_nodesets.append(Nodeset(name=nsn.replace((nodeset_prefix + "_"), "")))

	return scene_nodesets

def get_file_nodesets(nodesets_file, mode="names"):
	nodesets_file_info = []

	with open(nodesets_file, "r") as f:
		data = f.read()
		f.close()

		pattern = '(.*setAttr ".nodesetName" -type.*)'
		if mode == "nodes": pattern = '(.*setAttr ".nodesetNodes" -type.*)'

		regx = re.compile(pattern, re.MULTILINE)
		matches = regx.findall(data)
		if len(matches) > 0:
			for match in matches:
				if not nodeset_main_name in match:
					parts = filter(None, re.split('[";]+', match))
					if mode == "names":						
						nodesets_file_info.append(parts[len(parts)-1].replace((nodeset_prefix + "_"),""))
					elif mode == "nodes":
						nodesets_file_info.append(eval(parts[len(parts)-1]))

	if nodesets_file_info == "": return None
	else: return nodesets_file_info

#######################################
# execution

if __name__ == "__main__":
	# print create_nodeset(name="test")
	# print create_nodeset(name="testSel", selection=True)
	# print create_nodeset(name="testObjects", nodes=cmds.ls(selection=True))
	# ns_test1 = Nodeset(name="testObjects1", nodes=cmds.ls(selection=True))
	# ns_test2 = Nodeset(name="testObjects2")

	# ns_test2.set_name("testillo")

	# print ns_test2.get_nodes(fullPath=True)

	# print get_file_nodesets(cmds.file(expandName=True, q=True))
	# print get_file_nodesets(cmds.file(expandName=True, q=True), mode="nodes")

	scene_nodesets = get_scene_nodesets()
	pass