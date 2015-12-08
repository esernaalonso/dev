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

def restoreBakedAnimationFromLocatorsRun():
	bakedLocators = bake.getSelectedBakedLocators()
	bake.bakeAnimControlsToLocators(bakedLocators)

#######################################
# execution

if __name__ == "__main__": restoreBakedAnimationFromLocatorsRun()