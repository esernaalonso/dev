import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


mUtil = OpenMaya.MScriptUtil()

c1 = "pCube1"
c2 = "pCube2"
c3 = "pCube3"

r1 = cmds.xform(c1, q=True, ws=True, ro=True)
r2 = cmds.xform(c2, q=True, ws=True, ro=True)
r3 = cmds.xform(c3, q=True, ws=True, ro=True)

x3 = cmds.xform(c3, q=True, ws=True, m=True)

rDiff = [r2[0]-r1[0], r2[1]-r1[1], r2[2]-r1[2]]

print rDiff

rResult = [rDiff[0]+r3[0], rDiff[1]+r3[1], rDiff[2]+r3[2]]

print rResult

cmds.xform(c3, ws=True, ro=rResult)