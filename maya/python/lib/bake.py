#######################################
# imports

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.mel as mel
import math

import esa.maya.python.lib.rig as rig

reload(rig)

#######################################
# functionality

def getSelectedAnimControls():
	currSel = cmds.ls(selection=True)
	selectedControls = []

	if len(currSel) == 0:
		cmds.confirmDialog(t="Alert", message="No animation controls selected. Select one at least to bake animation.", button=["OK"], icon="warning")
	else:
		shapeList = cmds.ls(type="nurbsCurve")
		transformList = cmds.listRelatives(shapeList, parent=True, fullPath=False)

		selectedControls = list(set(currSel).intersection(transformList))

		if len(selectedControls) == 0:
			cmds.confirmDialog(t="Alert", message="No animation controls selected. Select one at least to bake animation.", button=["OK"], icon="warning")
	
	return selectedControls

def getSelectedBakedLocators():
	currSel = cmds.ls(selection=True)
	selectedControls = []

	if len(currSel) == 0:
		cmds.confirmDialog(t="Alert", message="No animation baked locators selected. Select one at least to restore baked animation.", button=["OK"], icon="warning")
	else:
		shapeList = cmds.ls(type="locator")
		transformList = cmds.listRelatives(shapeList, parent=True, fullPath=False)

		selectedControls = list(set(currSel).intersection(transformList))

		if len(selectedControls) == 0:
			cmds.confirmDialog(t="Alert", message="No animation baked locators selected. Select one at least to restore baked animation.", button=["OK"], icon="warning")
	
	return selectedControls

def getControlBakeLocator(animationControl):
	bakeLocator = animationControl + "_BAKE"

	if len(cmds.ls(bakeLocator)) == 0:
		bakeLocator = cmds.spaceLocator(n=bakeLocator)[0]

		# scale the locator
		cmds.setAttr((bakeLocator + ".scaleX"), 2)
		cmds.setAttr((bakeLocator + ".scaleY"), 2)
		cmds.setAttr((bakeLocator + ".scaleZ"), 2)
	
	return bakeLocator

def getBakeLocatorControl(bakedLocator):
	animControl = bakedLocator.replace("_BAKE", "")

	if len(cmds.ls(animControl)) == 0:
		return None
	else:	
		return animControl

def bakeLocatorsToAnimControls(controlsToBake):
	print "\nBaking Locators to Controls..."

	selBckp = cmds.ls(selection=True)

	start = int(cmds.playbackOptions(q=True, minTime=True))
	end = int(cmds.playbackOptions(q=True, maxTime=True))
	
	currentViewport = cmds.getPanel(wf=True)

	isolateState = cmds.isolateSelect(currentViewport, q=True, state=True)

	cmds.select(clear=True)
	cmds.isolateSelect(currentViewport, state=1)

	cmds.select(controlsToBake, replace=True)
	cmds.isolateSelect(currentViewport, addSelected=True )

	if len(controlsToBake) > 0:
		cmds.waitCursor(state=True)

		for i in range(start, end + 1):
			print ("\nCurrent Frame -> " + str(i))
			cmds.currentTime(i, update=True)

			for ctrl in controlsToBake:
				print ("\nControl -> " + ctrl)

				# gets the bake locator for this control or creates if not exists
				bakeLocator = getControlBakeLocator(ctrl)
				print ("Baking into Locator -> " + bakeLocator)

				# now this locator must be keyed and aligned along the timeline to the anim control creating keys by frame		

				#get the transform values of the control
				cmds.select(ctrl, replace=True)
				position = cmds.xform(query=True, translation=True, worldSpace=True)
				rotation = cmds.xform(query=True, rotation=True, worldSpace=True)
		
				# locates the locator
				cmds.setAttr((bakeLocator + ".translateX"), position[0])
				cmds.setAttr((bakeLocator + ".translateY"), position[1])
				cmds.setAttr((bakeLocator + ".translateZ"), position[2])
				cmds.setAttr((bakeLocator + ".rotateX"), rotation[0])
				cmds.setAttr((bakeLocator + ".rotateY"), rotation[1])
				cmds.setAttr((bakeLocator + ".rotateZ"), rotation[2])

				# creates the key for that frame
				cmds.select(bakeLocator, replace=True)
				cmds.setKeyframe()

		cmds.waitCursor(state=False)

	cmds.isolateSelect(currentViewport, state=isolateState)
	cmds.currentTime(start, update=True)

	cmds.select(clear=True)
	cmds.select(selBckp, replace=True)

	print "\n...Locators Baked to Controls\n"

def bakeAnimControlsToLocators(bakedLocators):
	print "\nBaking Controls to Locators..."

	selBckp = cmds.ls(selection=True)

	start = int(cmds.playbackOptions(q=True, minTime=True))
	end = int(cmds.playbackOptions(q=True, maxTime=True))
	
	currentViewport = cmds.getPanel(wf=True)

	isolateState = cmds.isolateSelect(currentViewport, q=True, state=True)

	cmds.select(clear=True)
	cmds.isolateSelect(currentViewport, state=1)

	cmds.select(bakedLocators, replace=True)
	cmds.isolateSelect(currentViewport, addSelected=True )

	if len(bakedLocators) > 0:
		cmds.waitCursor(state=True)

		for i in range(start, end + 1):
			print ("\nCurrent Frame -> " + str(i))
			cmds.currentTime(i, update=True)

			for loc in bakedLocators:
				print ("\nLocator -> " + loc)

				# gets the anim control for this bake locator
				animControl = getBakeLocatorControl(loc)

				if animControl is not None:
					print ("Baking into Locator -> " + animControl)
					# now this anim control must be keyed and aligned along the timeline to the bake locator creating keys by frame		

					#get the transform values of the locator
					cmds.select(loc, replace=True)
					bakedPosition = cmds.xform(query=True, translation=True, worldSpace=True)
					bakedRotation = cmds.xform(query=True, rotation=True, worldSpace=True)
			
					# locates the anim control					
					cmds.select(animControl, replace=True)
					cmds.xform(absolute=True, worldSpace=True, rotation=bakedRotation)
					cmds.xform(absolute=True, worldSpace=True, translation=bakedPosition)

					# creates the key for that frame
					cmds.select(animControl, replace=True)
					cmds.setKeyframe()
					
		cmds.waitCursor(state=False)

	cmds.isolateSelect(currentViewport, state=isolateState)
	cmds.currentTime(start, update=True)

	cmds.select(clear=True)
	cmds.select(selBckp, replace=True)

	print "\n...Controls Baked to Locators\n"

def bakeAnimControlsToCurve(curve, animControls, timeStart, timeEnd, timeStep=1, fakeNormal=None, startingControl=0, invert=False, animLayerName=None):

	mUtil = OpenMaya.MScriptUtil()

	if type(curve) is not list:
		curve = [curve]
		animControls = [animControls]
	if type(fakeNormal) is not list: fakeNormal = [fakeNormal]
	if type(startingControl) is not list: startingControl = [startingControl]
	if type(invert) is not list: invert = [invert]
	if type(animLayerName) is not list: animLayerName = [animLayerName]

	animControlsMatricesList = []
	animControlsMatricesOffsetList = []

	bakeAnimLayer = []
	percents = []

	cmds.currentTime(timeStart, update=True)

	for k in range(len(curve)):
		if animLayerName[k] == None: animLayerName[k] = "DynamicsBake"
		bakeAnimLayer.append(cmds.animLayer(animLayerName[k], sel=True, prf=True))

		percents.append([])

		# animCtrlRots = []
		animCtrlMatrices = []

		for i in range(len(animControls[k])):
			# adds the attributes to the anim layers
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".translateX"))
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".translateY"))
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".translateZ"))
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".rotateX"))
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".rotateY"))
			cmds.animLayer(bakeAnimLayer[k], edit=True, at=(animControls[k][i] + ".rotateZ"))

			# calculates the intial percent for echa anim control
			pInCurve = rig.getClosestPointOnCurve(curve[k], cmds.xform(animControls[k][i], q=True, ws=True, t=True))
			percent = rig.getPercentOfCurvePoint(curve[k], pInCurve)
			percents[k].append(percent)

			# store anim control initial matrix
			# animCtrlRots.append(cmds.xform(animControls[k][i], q=True, ws=True, ro=True))
			animCtrlMatrices.append(cmds.xform(animControls[k][i], q=True, ws=True, m=True))

		# inits the list of lists for the matrices
		animControlsMatricesList.append([])

		# first calculates the matrices offset between curve point and animation control for first frame
		animControlsInCurvesMatrices = rig.getAlignAnimControlsToCurveMatrices(curve[k], animControls[k], percents=percents[k], fakeNormal=fakeNormal[k], invert=invert[k])
				
		# calculate the offsets and store
		animControlsMatricesOffset = []
		for i in range(len(animControlsInCurvesMatrices)):
			curvePointMatrix = OpenMaya.MMatrix()
			mUtil.createMatrixFromList(animControlsInCurvesMatrices[i], curvePointMatrix)

			animCtrlMatrix = OpenMaya.MMatrix()
			mUtil.createMatrixFromList(animCtrlMatrices[i], animCtrlMatrix)
			
			offsetMatrix = animCtrlMatrix*curvePointMatrix.inverse()
			animControlsMatricesOffset.append(offsetMatrix)
			
		animControlsMatricesOffsetList.append(animControlsMatricesOffset)
		
	gMainProgressBar = mel.eval('$pb = $gMainProgressBar')
	limit = (timeEnd + 1 - timeStart)*len(curve)
	cmds.progressBar(gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status="First Pass: Bake Rig Dynamics Calculation", maxValue=limit)

	stop = False
	for i in range(timeStart, timeEnd + 1):
		cmds.currentTime(i, update=True)

		if (i==timeStart or i==timeEnd or (((i - timeStart) % timeStep) == 0)):

			for k in range(len(curve)):
				animControlsMatrices = rig.getAlignAnimControlsToCurveMatrices(curve[k], animControls[k], percents=percents[k], fakeNormal=fakeNormal[k], invert=invert[k])

				animControlsMatricesList[k].append(animControlsMatrices)

				if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
					stop = True
					break

				cmds.progressBar(gMainProgressBar, edit=True, step=1)

			if stop: break

		if stop: break

	if not stop:
		cmds.progressBar(gMainProgressBar, edit=True, beginProgress=True, progress=0, isInterruptable=True, status="Second Pass: Bake Rig Dynamics Apply", maxValue=limit)
		matricesCount = 0
		for i in range(timeStart, timeEnd + 1):
			cmds.currentTime(i, update=True)

			if (i==timeStart or i==timeEnd or (((i - timeStart) % timeStep) == 0)):

				for k in range(len(curve)):
					# new matrices calculation for the animation controls aplying the curve current matrices and the initial offsets
					newmatrices = []
					for j in range(len(animControls[k])):
						offsetMatrix = animControlsMatricesOffsetList[k][j]
						pointInCurveMatrix = OpenMaya.MMatrix()
						mUtil.createMatrixFromList(animControlsMatricesList[k][matricesCount][j], pointInCurveMatrix)
						newM = offsetMatrix*pointInCurveMatrix
						newMatrixList = [newM(0,0), newM(0,1), newM(0,2), newM(0,3), newM(1,0), newM(1,1), newM(1,2), newM(1,3), newM(2,0), newM(2,1), newM(2,2), newM(2,3), newM(3,0), newM(3,1), newM(3,2), newM(3,3)]
						newmatrices.append(newMatrixList)

					rig.alignAnimControlsToCurve(curve[k], animControls[k], percents=percents[k], startingControl=startingControl[k], fakeNormal=fakeNormal[k], forceMatrices=True, matrices=newmatrices, invert=invert[k])

					for j in range(startingControl[k], len(animControls[k])):
						# creates the keys in the animation layer
						cmds.setKeyframe(animControls[k][j], at="translateX", animLayer=bakeAnimLayer[k])
						cmds.setKeyframe(animControls[k][j], at="translateY", animLayer=bakeAnimLayer[k])
						cmds.setKeyframe(animControls[k][j], at="translateZ", animLayer=bakeAnimLayer[k])
						cmds.setKeyframe(animControls[k][j], at="rotateX", animLayer=bakeAnimLayer[k])
						cmds.setKeyframe(animControls[k][j], at="rotateY", animLayer=bakeAnimLayer[k])
						cmds.setKeyframe(animControls[k][j], at="rotateZ", animLayer=bakeAnimLayer[k])

					if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) :
						stop = True
						break

					cmds.progressBar(gMainProgressBar, edit=True, step=1)

				if stop: break

				matricesCount += 1

			if stop: break

	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

def bakeACPdynamics(ACPnames, dynamicTypes, timeStart, timeEnd, timeStep=1, fakeNormal=None, startingControl=0):
	if type(ACPnames) is not list: ACPnames = [ACPnames]
	if type(dynamicTypes) is not list: dynamicTypes = [dynamicTypes]

	curves = []
	animControls = []
	fakeNormals = []
	startingControls = []
	inverts = []
	animLayerNames = []

	errorMessage = ""

	for ACP in ACPnames:
		if "tail" in dynamicTypes:
			curve_tail = ACP + ":tailSecondaryCurve_CRV"
			animControls_tail = cmds.ls(ACP + ":tail?_CTRL")

			if len(cmds.ls(curve_tail)) > 0 and len(animControls_tail) > 0:
				curves.append(curve_tail)
				animControls.append(animControls_tail)
				fakeNormals.append(fakeNormal)
				startingControls.append(startingControl)
				inverts.append(False)
				animLayerNames.append(ACP + ":tail_dynamicsBake")
			else:
				errorMessage += ACP + " doesn't exist or has no tail\n"

		if "ears" in dynamicTypes:
			curve_ear_l = ACP + ":l_earSplineCurve_CRV"
			animControls_ear_l = cmds.ls(ACP + ":l_ear?_CTRL")

			if len(cmds.ls(curve_ear_l)) > 0 and len(animControls_ear_l) > 0:
				curves.append(curve_ear_l)
				animControls.append(animControls_ear_l)
				fakeNormals.append(fakeNormal)
				startingControls.append(startingControl)
				inverts.append(True)
				animLayerNames.append(ACP + ":ear_L_dynamicsBake")
			else:
				errorMessage += ACP + " doesn't exist or has no L ear\n"

			curve_ear_r = ACP + ":r_earSplineCurve_CRV"
			animControls_ear_r = cmds.ls(ACP + ":r_ear?_CTRL")

			if len(cmds.ls(curve_ear_r)) > 0 and len(animControls_ear_r) > 0:
				curves.append(curve_ear_r)
				animControls.append(animControls_ear_r)
				fakeNormals.append(fakeNormal)
				startingControls.append(startingControl)
				inverts.append(False)
				animLayerNames.append(ACP + ":ear_R_dynamicsBake")
			else:
				errorMessage += ACP + " doesn't exist or has no R ear\n"

		if "l_ear" in dynamicTypes:
			curve_ear_l = ACP + ":l_earSplineCurve_CRV"
			animControls_ear_l = cmds.ls(ACP + ":l_ear?_CTRL")

			if len(cmds.ls(curve_ear_l)) > 0 and len(animControls_ear_l) > 0:
				curves.append(curve_ear_l)
				animControls.append(animControls_ear_l)
				fakeNormals.append(fakeNormal)
				startingControls.append(startingControl)
				inverts.append(True)
				animLayerNames.append(ACP + ":ear_L_dynamicsBake")
			else:
				errorMessage += ACP + " doesn't exist or has no L ear\n"

		if "r_ear" in dynamicTypes:
			curve_ear_r = ACP + ":r_earSplineCurve_CRV"
			animControls_ear_r = cmds.ls(ACP + ":r_ear?_CTRL")

			if len(cmds.ls(curve_ear_r)) > 0 and len(animControls_ear_r) > 0:
				curves.append(curve_ear_r)
				animControls.append(animControls_ear_r)
				fakeNormals.append(fakeNormal)
				startingControls.append(startingControl)
				inverts.append(False)
				animLayerNames.append(ACP + ":ear_R_dynamicsBake")
			else:
				errorMessage += ACP + " doesn't exist or has no R ear\n"

		# Branch
		for dynType in dynamicTypes:
			if "Branch" in dynType:
				side = dynType.split("_")[0]
				curve_branch = ACP + ":" + dynType + "_ASplineCurve_CRV"
				animControls_branch = cmds.ls(ACP + ":" + dynType + "_??_CTRL")
				
				if len(cmds.ls(curve_branch)) > 0 and len(animControls_branch) > 0:
					curves.append(curve_branch)
					animControls.append(animControls_branch)
					fakeNormals.append(fakeNormal)
					startingControls.append(startingControl)
					inverts.append(False)
					animLayerNames.append(ACP + ":" + dynType + "_dynamicsBake")
				else:
					errorMessage += ACP + " doesn't exist or has no " + dynType + "\n"

	if len(curves) > 0:		
		bakeAnimControlsToCurve(curves, animControls, timeStart, timeEnd, timeStep=timeStep, fakeNormal=fakeNormals, startingControl=startingControls, invert=inverts, animLayerName=animLayerNames)

	cmds.currentTime(timeStart, update=True)

	for aControls in animControls:
		if len(aControls) > 0:
			if len(cmds.listAttr(aControls[0], st="enableDynamics")) > 0:
				try:
					cmds.setAttr((aControls[0] + ".enableDynamics"), 0)
				except:
					mssgAdd = ACP + ":" + dynType + ".enableDynamics is locked and cannot be disabled after bake. You should disable it manually in the rig main control.\n"
					if mssgAdd not in errorMessage: errorMessage += mssgAdd

	if errorMessage != "":
		cmds.confirmDialog(t="Alert", message=errorMessage, button=["OK"], icon="warning")

def bakeACPtailDynamics(ACPname, timeStart, timeEnd, timeStep=1, fakeNormal=None, startingControl=0):
	bakeACPdynamics(ACPname, "tail", timeStart, timeEnd, timeStep=timeStep, fakeNormal=fakeNormal, startingControl=startingControl)

def bakeACPearsDynamics(ACPname, timeStart, timeEnd, timeStep=1, fakeNormal=None, startingControl=0):
	bakeACPdynamics(ACPname, "ears", timeStart, timeEnd, timeStep=timeStep, fakeNormal=fakeNormal, startingControl=startingControl)

#######################################
# execution

if __name__ == "__main__":
	pass