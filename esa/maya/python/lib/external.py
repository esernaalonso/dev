#######################################
# imports

import maya.cmds as cmds
import maya.mel as mel

import os

import esa.maya.python.lib.io as io

reload(io)

#######################################
# functionality

def getExternalRootFolder():
	extFolder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "modules", "external")
	return extFolder

# def loadBonusTools():
# 	print "\nLoading Custom Bonus Tools..."

# 	# adding the bonusTools paths to MAYA_SCRIPT_PATH

# 	bonusToolsPath = os.path.join(getExternalRootFolder(), "bonusTools")
# 	bonusToolsPaths = io.getRecursiveSubdfolders(bonusToolsPath)

# 	for pth in bonusToolsPaths:
# 		if not pth.replace("\\","\\\\") in os.environ["MAYA_SCRIPT_PATH"]:
# 			os.environ["MAYA_SCRIPT_PATH"] = os.environ["MAYA_SCRIPT_PATH"] + ":" + pth.replace("\\","\\\\")
# 		print ('Adding "' + pth + '" to MAYA_SCRIPT_PATH')

# 	bonusToolsMenuPath = os.path.join(bonusToolsPath, "scripts-2015", "bonusToolsMenu.mel")
# 	mel.eval('source "' + bonusToolsMenuPath.replace("\\","\\\\") + '";')
# 	mel.eval("bonusToolsMenu;")

# 	print "Custom Bonus Tools loaded"

# def loadAdvancedSkeleton4():
# 	print "\nLoading Advanced Skeleton 4..."

# 	# advancedSkeleton4File = os.path.join(getExternalRootFolder(), "AdvancedSkeleton4", "AdvancedSkeleton4.mel")
# 	# mel.eval('source "' + advancedSkeleton4File.replace("\\","\\\\") + '";')
# 	# mel.eval("AdvancedSkeleton4;")

# 	advancedSkeleton4FileMelLoader = os.path.join(os.path.dirname(__file__), "external_loadAdvancedSkeleton4.mel")
# 	mel.eval('source "' + advancedSkeleton4FileMelLoader.replace("\\","\\\\") + '";')

# 	print "Advanced Skeleton 4 loaded"

# def loadAdvancedSkeleton5():
# 	print "\nLoading Advanced Skeleton 5..."

# 	advancedSkeleton5FileMelLoader = os.path.join(os.path.dirname(__file__), "external_loadAdvancedSkeleton5.mel")
# 	mel.eval('source "' + advancedSkeleton5FileMelLoader.replace("\\","\\\\") + '";')

# 	print "Advanced Skeleton 5 loaded"

#######################################
# execution

if __name__ == "__main__":
	# loadBonusTools()
	pass