#######################################
# imports

import maya.cmds as cmds

import esa.maya.python.lib.bake as bake

reload(bake)

#######################################
# attributes

permission = "artist"

#######################################
# functionality

def bakeAnimationToLocatorsRun():
	selectedControls = bake.getSelectedAnimControls()
	bake.bakeLocatorsToAnimControls(selectedControls)

#######################################
# execution

if __name__ == "__main__": bakeAnimationToLocatorsRun()