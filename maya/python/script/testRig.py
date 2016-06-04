#######################################
# imports

import maya.cmds as cmds

import esa.maya.python.lib.rig as rig

reload(rig)

#######################################
# attributes

permission = "developer"

#######################################
# functionality

def testRigRun():
	print "test rig"

#######################################
# execution

if __name__ == "__main__": testRigRun()