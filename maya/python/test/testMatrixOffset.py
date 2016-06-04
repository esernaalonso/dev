import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


mUtil = OpenMaya.MScriptUtil()

c1 = "pCube1"
c2 = "pCube2"
c3 = "pCube3"

x1 = cmds.xform(c1, q=True, ws=True, m=True)
x2 = cmds.xform(c2, q=True, ws=True, m=True)
x3 = cmds.xform(c3, q=True, ws=True, m=True)

print x1
print x2
print x3

m1 = OpenMaya.MMatrix()
m2 = OpenMaya.MMatrix()
m3 = OpenMaya.MMatrix()

mUtil.createMatrixFromList(x1, m1)
mUtil.createMatrixFromList(x2, m2)
mUtil.createMatrixFromList(x3, m3)

print m1
print m2
print m3

mDiff = m2*m1.inverse()

print mDiff

mResult = mDiff*m3

print mResult

mList = [
mResult(0,0), mResult(0,1), mResult(0,2), mResult(0,3),
mResult(1,0), mResult(1,1), mResult(1,2), mResult(1,3),
mResult(2,0), mResult(2,1), mResult(2,2), mResult(2,3),
mResult(3,0), mResult(3,1), mResult(3,2), mResult(3,3)
]

cmds.xform(c3, ws=True, m=mList)