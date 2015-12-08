#######################################
# imports

import maya.cmds as cmds

import esa.maya.python.lib.deploy as deploy

reload(deploy)

#######################################
# attributes

permission = "developer"

#######################################
# functionality

def deployCurrentToolCageRun():
	deploy.deployCurrentToolCageDev()
	cmds.confirmDialog(t="msg", message="Current ToolGage DEV deployed to TOOLS.", button=["OK"]) 

#######################################
# execution

if __name__ == "__main__": deployCurrentToolCageRun()