#######################################
# imports

import maya.cmds as cmds

#######################################
# attributes

permission = "artist"

#######################################
# functionality

def geometryNormalConstraintRun():
	currentSelection = cmds.ls(selection=True)

	if len(currentSelection) > 1:
		ground = currentSelection[len(currentSelection)- 1]

		for i in range(len(currentSelection) - 1):
			cmds.geometryConstraint(ground , currentSelection[i])
			cmds.normalConstraint(ground , currentSelection[i], aim=[0,1,0], u=[0,1,0], wut="Vector", wu=[0,1,0])
	else:
		cmds.confirmDialog(t="Warning", message="You must select at least two geometry objects. Last object will always be considered the ground target", button=["OK"], icon="warning")

#######################################
# execution

if __name__ == "__main__": geometryNormalConstraintRun()