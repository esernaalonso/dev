#######################################
# imports

import maya.cmds as cmds

import re

#######################################
# functionality

def getSceneSelectedACPnames():
	ACPnames = []

	selObjects = cmds.ls(selection=True)
	for selObj in selObjects:
		nameParts = selObj.split(":")
		if len(nameParts) == 3:
			ACPname = selObj.replace(nameParts[len(nameParts) - 1], "")
			if ACPname[len(ACPname) - 1] == ":": ACPname = ACPname[:-1]
			if ACPname not in ACPnames: ACPnames.append(ACPname)

	return ACPnames

def getSceneSelectedACPdynamicSystemsNames():
	ACPdynSystemsNames = []

	selObjects = cmds.ls(selection=True)
	for selObj in selObjects:
		nameParts = selObj.split(":")
		if len(nameParts) == 3:
			ACPname = selObj.replace(nameParts[len(nameParts) - 1], "")
						
			dynSysName = None

			if "tail" in selObj: dynSysName = ACPname + "tail"
			if "l_ear" in selObj: dynSysName = ACPname + "l_ear"
			if "r_ear" in selObj: dynSysName = ACPname + "r_ear"

			if dynSysName is not None and dynSysName not in ACPdynSystemsNames: ACPdynSystemsNames.append(dynSysName)

	# BRANCHES
	selObjectsNames = "\n".join(selObjects)
	
	regx = re.compile(("(.*):((._)?.*Branch_.*)_.*_.*"), re.MULTILINE)
	matches = regx.findall(selObjectsNames)
	for m in matches:
		dynSysName = m[0] + ":" + m[1]
		if dynSysName not in ACPdynSystemsNames: ACPdynSystemsNames.append(dynSysName)

	return ACPdynSystemsNames

def getSceneACPdynamicSystemsNames(selection=False):
	dynamicSystemsNames = []

	# TAIL
	tailPattern = "tailSecondaryCurve_CRV"
	tails = cmds.ls(tailPattern, r=True)
	for tail in tails:
		ACPname = tail.replace(tailPattern, "")
		if ACPname[len(ACPname) - 1] == ":": ACPname = ACPname[:-1]
		ACPname += ":tail"
		if ACPname not in dynamicSystemsNames: dynamicSystemsNames.append(ACPname)

	# earsPattern = "?_earSplineCurve_CRV"
	# ears = cmds.ls(earsPattern, r=True)
	# for ear in ears:
	# 	ACPname = ear.replace((earsPattern.replace("?", "l")), "")
	# 	ACPname = ACPname.replace((earsPattern.replace("?", "r")), "")
	# 	if ACPname[len(ACPname) - 1] == ":": ACPname = ACPname[:-1]
	# 	ACPname += ":ears"
	# 	if ACPname not in dynamicSystemsNames: dynamicSystemsNames.append(ACPname)

	# L EAR
	l_earPattern = "l_earSplineCurve_CRV"
	ears = cmds.ls(l_earPattern, r=True)
	for ear in ears:
		ACPname = ear.replace(l_earPattern, "")
		if ACPname[len(ACPname) - 1] == ":": ACPname = ACPname[:-1]
		ACPname += ":l_ear"
		if ACPname not in dynamicSystemsNames: dynamicSystemsNames.append(ACPname)

	# R REAR
	r_earPattern = "r_earSplineCurve_CRV"
	ears = cmds.ls(r_earPattern, r=True)
	for ear in ears:
		ACPname = ear.replace(r_earPattern, "")
		if ACPname[len(ACPname) - 1] == ":": ACPname = ACPname[:-1]
		ACPname += ":r_ear"
		if ACPname not in dynamicSystemsNames: dynamicSystemsNames.append(ACPname)

	# BRANCHES
	allObjects = cmds.ls()
	allObjectsNames = "\n".join(allObjects)
	
	regx = re.compile(("(.*):((._)?.*Branch_.*)_ASplineCurve_CRV"), re.MULTILINE)
	matches = regx.findall(allObjectsNames)
	for m in matches:
		dynSysName = m[0] + ":" + m[1]
		if dynSysName not in dynamicSystemsNames: dynamicSystemsNames.append(dynSysName)

	if selection:
		sceneSelACPdynSys = getSceneSelectedACPdynamicSystemsNames()
		dynamicSystemsNames = list(set(sceneSelACPdynSys) & set(dynamicSystemsNames))

	dynamicSystemsNames.sort()

	return dynamicSystemsNames	

#######################################
# execution

if __name__ == "__main__":
	print (getSceneACPdynamicSystemsNames(selection=False))
	pass