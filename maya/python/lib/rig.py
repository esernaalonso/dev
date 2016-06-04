#######################################
# imports

import maya.OpenMaya as om
import maya.cmds as cmds

import os, sys

import esa.maya.python.lib.units as units
import esa.maya.python.lib.mathext as mathext

reload(units)
reload(mathext)

#######################################
# functionality

def combineShapes(objects):
	shapes = []
	for i in range(1, len(objects)):
		cmds.xform(objects[i], t=[0,0,0], ws=True)
		cmds.makeIdentity(objects[i], apply=True, t=1, r=1, s=1, n=0)
		objShapes = cmds.listRelatives(objects[i], s=True, pa=True)
		for j in range(len(objShapes)):
			shapes.append(objShapes[j])

	cmds.refresh()

	for i in range(len(shapes)):
		cmds.parent(shapes[i], objects[0], r=True, s=True)

	for i in range(1, len(objects)):
		cmds.delete(objects[i])

def setPivotPosition(objects):
	cmds.xform(objects, piv=[0,0,0], ws=True)

# curves functions

def getClosestPointOnCurve(curve, pointInSpace):
	tempList = om.MSelectionList()
	tempList.add(curve)
	curveObj = om.MObject()
	tempList.getDependNode(0, curveObj)  # puts the 0 index of tempList's depend node into curveObj

	# get the dagpath of the object
	dagpath = om.MDagPath()
	tempList.getDagPath(0, dagpath)

	# define the curve object as type MFnNurbsCurve
	curveMF = om.MFnNurbsCurve(dagpath)

	# what's the input point (in world)
	point = om.MPoint( pointInSpace[0], pointInSpace[1], pointInSpace[2])

	# define the parameter as a double * (pointer)
	prm = om.MScriptUtil()
	pointer = prm.asDoublePtr()
	om.MScriptUtil.setDouble (pointer, 0.0)

	# set tolerance
	tolerance = .00000001

	# set the object space
	space = om.MSpace.kObject

	# result will be the worldspace point
	result = om.MPoint()
	result = curveMF.closestPoint (point, pointer,  0.0, space)

	position = [(result.x), (result.y), (result.z)]
	curvePoint = om.MPoint ((result.x), (result.y), (result.z))

	return [(result.x), (result.y), (result.z)]

def getPercentOfCurvePoint(curve, curvePoint, curveSteps=1000, tolerance=0.01):
	percentage = None
	
	for i in range(curveSteps + 1):
		currPercent = (1.0/curveSteps)*i
		currPoint = cmds.pointOnCurve(curve, ch=False, pr=currPercent, p=True)

		dist = abs(sqrt((curvePoint[0]-currPoint[0])^2 + (curvePoint[1]-currPoint[1])^2 + (curvePoint[2]-currPoint[2])^2))

		if dist <= tolerance:
			percentage = currPercent
			break

	return percentage

def getPointOnCurveMatrix(curve, percent, tangentAxis="Y", normalAxis="Z", fakeNormal=None, invert=False):
	# get the point information
	pos = cmds.pointOnCurve(curve, ch=False, pr=percent, p=True)
	tan = cmds.pointOnCurve(curve, ch=False, pr=percent, nt=True)
	nor = cmds.pointOnCurve(curve, ch=False, pr=percent, nn=True) #not used

	# convert the point pos to internal unots
	pos[0] = units.unitsConvertUItoInternal(pos[0])
	pos[1] = units.unitsConvertUItoInternal(pos[1])
	pos[2] = units.unitsConvertUItoInternal(pos[2])

	# normalize the other vectors
	tan = mathext.normalize(tan)
	
	fakeNor = nor
	if fakeNormal is not None: fakeNor = fakeNormal

	# creating binormal and normal from 
	bin = mathext.normalize(mathext.cross(tan, fakeNor))
	nor = mathext.normalize(mathext.cross(bin, tan))	

	# creates the new matrix
	xVec = bin
	yVec = bin
	zVec = bin

	if tangentAxis == "X": xVec = tan
	elif tangentAxis == "Y": yVec = tan
	elif tangentAxis == "Z": zVec = tan

	if normalAxis == "X": xVec = nor
	elif normalAxis == "Y": yVec = nor
	elif normalAxis == "Z": zVec = nor

	mtx = [xVec[0], xVec[1], xVec[2], 0.0, yVec[0], yVec[1], yVec[2], 0.0, zVec[0], zVec[1], zVec[2], 0.0, pos[0], pos[1], pos[2], 1.0]

	if invert:
		for i in range(len(mtx)):
			mtx[i] = -mtx[i]

	# mtx = [[0 for x in range(4)] for x in range(4)]
	# mtx[0] = [bin[0], bin[1], bin[2], 0.0]
	# mtx[1] = [tan[0], tan[1], tan[2], 0.0]
	# mtx[2] = [nor[0], nor[1], nor[2], 0.0]
	# mtx[3] = [pos[0], pos[1], pos[2], 1.0]

	# return the new matrix
	return mtx

def getAlignAnimControlsToCurveMatrices(curve, animControls, percents=None, fakeNormal=None, invert=False):
	curvePointsMatrix = []
	numPoints = len(animControls)

	for i in range(len(animControls)):
		if percents is None or percents[i] is None:
			pInCurve = getClosestPointOnCurve(curve, cmds.xform(animControls[i], q=True, ws=True, t=True))
			percent = getPercentOfCurvePoint(curve, pInCurve, curveSteps=100, tolerance=0.01)

			if percent is None:
				percent = getPercentOfCurvePoint(curve, pInCurve, curveSteps=1000, tolerance=0.01)

			if percent is None:
				percent = (1.0/(numPoints - 1))*i
		else:
			percent = percents[i]

		if fakeNormal is None:
			normalAxis = "Z"
			mtx = cmds.xform(animControls[i], q=True, ws=True, matrix=True)

			if normalAxis == "Z": fakeNormal = ([mtx[8], mtx[9], mtx[10]])
			elif normalAxis == "Y": fakeNormal = ([mtx[4], mtx[5], mtx[6]])
			elif normalAxis == "X": fakeNormal = ([mtx[0], mtx[1], mtx[2]])
			
		curvePointsMatrix.append(getPointOnCurveMatrix(curve, percent, fakeNormal=fakeNormal, invert=invert))
	
	return curvePointsMatrix	

def alignAnimControlsToCurve(curve, animControls, percents=None, startingControl=0, fakeNormal=None, forceMatrices=False, matrices=None, invert=False):

	if (not forceMatrices) or (matrices is None) or (len(matrices) < (len(animControls) - startingControl)):
		matrices = getAlignAnimControlsToCurveMatrices(curve, animControls, percents=percents, fakeNormal=fakeNormal, invert=invert)
	
	for i in range(startingControl, len(animControls)):
		cmds.xform(animControls[i], ws=True, m=matrices[i])

#######################################
# execution

if __name__ == "__main__":
	combineShapes(cmds.ls(selection=True))
	# setPivotPosition(cmds.ls(selection=True))
	pass