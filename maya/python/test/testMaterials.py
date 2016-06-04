import maya.cmds as cmds

currSel = cmds.ls(selection=True)

for obj in currSel:
	print obj
	shaders = cmds.listConnections(cmds.listHistory(obj,f=1),type='lambert')
	print shaders
	print "-----------------------------"
