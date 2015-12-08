#######################################
# imports

import esa.maya.python.lib.external as external

#######################################
# attributes

permission = "developer"

#######################################
# functionality

def initBonusToolsRun():
	external.loadBonusTools()

#######################################
# execution

if __name__ == "__main__": initBonusToolsRun()