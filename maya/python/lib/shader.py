#######################################
# imports

import maya.cmds as cmds
import maya.mel as mel
import os

import esa.maya.python.tool.misc.nodeEditor as nodeEditor

reload(nodeEditor)

#######################################
# functionality

def set_objects_no_material(objects):
	for obj in objects:
		print obj
		shapes = cmds.listRelatives(obj, shapes=True, path=True)
		for sh in shapes:
			cmds.disconnectAttr(sh + ".instObjGroups[0]", "initialShadingGroup.dagSetMembers[0]")

def getImagePlaneFilePath(imagePlane):
	return cmds.getAttr(imagePlane+".imageName")

def getCameraConnectedImagePlanes(jobCamera):
	# if we have camera transform then go to camera shape 
	if cmds.nodeType(jobCamera) == 'transform':
		jobCamera = cmds.listRelatives(jobCamera, s=True, c=True)[0]

	if cmds.nodeType(jobCamera) != 'camera': 
		cmds.error("%s is not a camera node" %jobCamera)

	# get all the imageplane nodes connected to image plane
	imagePlanes = cmds.listConnections(jobCamera + '.imagePlane', source = True, type = 'imagePlane') or []

	return imagePlanes

def getAllSceneImagePlanes():
	allImagePlanes = []

	sceneCameras = cmds.ls(cameras=True )
	for cam in sceneCameras:
		imgPlanes = getCameraConnectedImagePlanes(cam)
		allImagePlanes.extend(imgPlanes)

	return allImagePlanes

def applyUseBackgroundShader(objectsList):
	# open node editor to avoid a bug that makes new nodes not update the image sequence
	nodeEditor.nodeEditorRun()

	# create the nodes
	useBackgroundShader = "projectionManagerUseBackground"
	exists = len(cmds.ls(useBackgroundShader)) > 0
	if not exists:
		useBackgroundShader = cmds.shadingNode("useBackground", asShader=True, name="projectionManagerUseBackground")
	
	# apply the shader
	cmds.select(objectsList)
	cmds.hyperShade(a=useBackgroundShader)

	# close the node editor
	nodeEditor.nodeEditorClose()

def applyLambertBackgroundShader(objectsList, imagePlane):
	# open node editor to avoid a bug that makes new nodes not update the image sequence
	nodeEditor.nodeEditorRun()

	lambertShader = "projectionManagerBackgroundLambert_" + (imagePlane.replace("->", "_"))

	# create the nodes
	exists = len(cmds.ls(lambertShader)) > 0
	if not exists:
		lambertShader = cmds.shadingNode("lambert", asShader=True, name=lambertShader)
		projectionNode = cmds.shadingNode("projection", asUtility=True, name="projectionManagerProjection")
		fileNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True, name="projectionManagerFile")
		# timeToUnit = cmds.shadingNode("timeToUnitConversion", asUtility=True, name="projectionManagerUnitConversion")
		
		# connect the nodes and config attributes
		cmds.connectAttr((projectionNode + ".outColor"), (lambertShader + ".color"))

		# cmds.setAttr((projectionNode + ".projType"), 0)
		cmds.setAttr((projectionNode + ".projType"), 8)

		cameraName = imagePlane.split("->")[0]
		cmds.connectAttr((cameraName + ".message"), (projectionNode + ".linkedCamera"))	  
		cmds.connectAttr((fileNode + ".outColor"), (projectionNode + ".image"))

		platePath = getImagePlaneFilePath(imagePlane)
		cmds.setAttr((fileNode + ".fileTextureName"), platePath, type="string")
		# cmds.setAttr((fileNode + ".useFrameExtension"), 0)
		cmds.setAttr((fileNode + ".useFrameExtension"), 1)
		
		# cmds.connectAttr(("time1.outTime"), (timeToUnit + ".input"))
		# cmds.setAttr((timeToUnit + ".conversionFactor"), 0.004)
		# cmds.connectAttr((timeToUnit + ".output"), (fileNode + ".frameExtension"))

		cmds.expression(string=(fileNode + ".frameExtension=frame"), name="projectionExpression")

	# apply the shader
	cmds.select(objectsList)
	cmds.hyperShade(a=lambertShader)

	# close the node editor
	nodeEditor.nodeEditorClose()

def applySurfaceBackgroundShader(objectsList, imagePlane):
	# open node editor to avoid a bug that makes new nodes not update the image sequence
	nodeEditor.nodeEditorRun()

	# shader name
	surfaceShader = "projectionManagerSurface_" + (imagePlane.replace("->", "_"))

	# create the nodes
	exists = len(cmds.ls(surfaceShader)) > 0
	if not exists:
		surfaceShader = cmds.shadingNode("surfaceShader", asShader=True, name=surfaceShader)
		projectionNode = cmds.shadingNode("projection", asUtility=True, name="projectionManagerProjection")
		fileNode = cmds.shadingNode("file", asTexture=True, isColorManaged=True, name="projectionManagerFile")
		
		# connect the nodes and config attributes
		cmds.connectAttr((projectionNode + ".outColor"), (surfaceShader + ".outColor"))

		# cmds.setAttr((projectionNode + ".projType"), 0)
		cmds.setAttr((projectionNode + ".projType"), 8)

		cameraName = imagePlane.split("->")[0]
		cmds.connectAttr((cameraName + ".message"), (projectionNode + ".linkedCamera"))
		cmds.connectAttr((fileNode + ".outColor"), (projectionNode + ".image"))

		platePath = getImagePlaneFilePath(imagePlane)
		cmds.setAttr((fileNode + ".fileTextureName"), platePath, type="string")
		# cmds.setAttr((fileNode + ".useFrameExtension"), 0)
		cmds.setAttr((fileNode + ".useFrameExtension"), 1)
			
		cmds.expression(string=(fileNode + ".frameExtension=frame"), name="projectionExpression")
	
	# apply the shader
	cmds.select(objectsList)
	cmds.hyperShade(a=surfaceShader)

	# close the node editor
	nodeEditor.nodeEditorClose()

def applyGreenScreenShader(objectsList):
	# create the nodes
	lambertShader = "projectionManagerGreenLambert"
	exists = len(cmds.ls(lambertShader)) > 0
	if not exists:
		lambertShader = cmds.shadingNode("lambert", asShader=True, name="projectionManagerGreenLambert")

		# connect the nodes and config attributes
		cmds.setAttr((lambertShader + ".color"), 0.0, 1.0, 0.0, type = 'double3')
		cmds.setAttr((lambertShader + ".ambientColor"), 1.0, 1.0, 1.0, type = 'double3')

	# apply the shader
	cmds.select(objectsList)
	cmds.hyperShade(a=lambertShader)

def applyGreenScreenShaderFx(objectsList):
	# create the nodes
	shaderfxShader = "projectionManagerGreenShaderFx"
	exists = len(cmds.ls(shaderfxShader)) > 0
	if not exists:
		mel.eval('source "' + os.path.dirname(__file__) + '/projectionManagerGreenShaderFx.mel"')
		shaderfxShader = cmds.ls(selection=True)[0]
	
		# connect the nodes and config attributes
		# nothing to do here

	# apply the shader
	cmds.select(clear=True)
	cmds.select(objectsList)
	cmds.hyperShade(a=shaderfxShader)

def applyDefaultShader(objectsList):
	# create the nodes
	lambertShader = "projectionManagerDefaultLambert"
	exists = len(cmds.ls(lambertShader)) > 0
	if not exists:
		lambertShader = cmds.shadingNode("lambert", asShader=True, name="projectionManagerDefaultLambert")

	# apply the shader
	cmds.select(objectsList)
	cmds.hyperShade(a=lambertShader)

#######################################
# execution

if __name__ == "__main__":
	# print ('source "' + os.path.dirname(__file__) + '/projectionManagerGreenShaderFx.mel"')
	# print (getAllSceneImagePlanes())
	# currSel = cmds.ls(selection=True)
	# applyGreenScreenShaderFx(currSel)
	pass