#######################################
# imports

import maya.cmds as cmds

import esa.maya.python.lib.rig as rig

reload(rig)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

def combineShapesRun():
	rig.combineShapes(cmds.ls(selection=True))

#######################################
# execution

if __name__ == "__main__": combineShapesRun()