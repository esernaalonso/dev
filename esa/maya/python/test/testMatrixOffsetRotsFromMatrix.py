import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import math

mUtil = OpenMaya.MScriptUtil()

c1 = "pCube1"
c2 = "pCube2"
c3 = "pCube3"

x1 = cmds.xform(c1, q=True, ws=True, m=True)
r1 = cmds.xform(c2, q=True, ws=True, ro=True)
print x1
print r1

auxMatrix = OpenMaya.MMatrix()
mUtil.createMatrixFromList(x1, auxMatrix)
mTransformMtx = OpenMaya.MTransformationMatrix(auxMatrix)
eulerRot = mTransformMtx.eulerRotation()
angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
print angles

ofs = [r1[0] - angles[0], r1[1] - angles[1], r1[2] - angles[2]]
print ofs

r2 = cmds.xform(c3, q=True, ws=True, ro=True)

rResult = [ofs[0]+r2[0], ofs[1]+r2[1], ofs[2]+r2[2]]

print rResult

cmds.xform(c3, ws=True, ro=rResult)