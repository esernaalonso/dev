import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math

mUtil = OpenMaya.MScriptUtil()

crv = ["pCube1", "pCube2", "pCube3"]
anim = ["pCube4", "pCube5", "pCube6"]
crv2 = ["pCube7", "pCube8", "pCube9"]

print crv
print anim
print crv2
print "----------"

crvX = [(cmds.xform(crv[i], q=True, ws=True, m=True)) for i in range(len(crv))]
animX = [(cmds.xform(anim[i], q=True, ws=True, m=True)) for i in range(len(anim))]
crv2X = [(cmds.xform(crv2[i], q=True, ws=True, m=True)) for i in range(len(crv2))]

print crvX
print animX
print crv2X
print "----------"

crvR = [(cmds.xform(crv[i], q=True, ws=True, ro=True)) for i in range(len(crv))]
animR = [(cmds.xform(anim[i], q=True, ws=True, ro=True)) for i in range(len(anim))]
crv2R = [(cmds.xform(crv2[i], q=True, ws=True, ro=True)) for i in range(len(crv2))]

# print crvR
# print animR
# print crv2R
# print "----------"

crvM = []
animM = []
crv2M = []

for i in range(len(crv)):
	auxMatrix = OpenMaya.MMatrix()
	mUtil.createMatrixFromList(crvX[i], auxMatrix)
	crvM.append(auxMatrix)

	auxMatrix = OpenMaya.MMatrix()
	mUtil.createMatrixFromList(animX[i], auxMatrix)
	animM.append(auxMatrix)

	auxMatrix = OpenMaya.MMatrix()
	mUtil.createMatrixFromList(crv2X[i], auxMatrix)
	crv2M.append(auxMatrix)

print crvM
print animM
print crv2M
print "----------"

ofsM = [(animM[i]*crvM[i].inverse()) for i in range(len(crv))]

print ofsM
print "----------"

newM = [(ofsM[i]*crv2M[i]) for i in range(len(crv))]

print newM
print "----------"

newX = []
for i in range(len(crv)):
	mList = [
	newM[i](0,0), newM[i](0,1), newM[i](0,2), newM[i](0,3),
	newM[i](1,0), newM[i](1,1), newM[i](1,2), newM[i](1,3),
	newM[i](2,0), newM[i](2,1), newM[i](2,2), newM[i](2,3),
	newM[i](3,0), newM[i](3,1), newM[i](3,2), newM[i](3,3)
	]
	newX.append(mList)

print newX
print "----------"

for i in range(len(crv)):
	cmds.xform(anim[i], ws=True, m=newX[i])