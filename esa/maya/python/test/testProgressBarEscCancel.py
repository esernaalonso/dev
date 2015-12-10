import maya.cmds as cmds
import maya.mel as mel

gMainProgressBar = mel.eval('$pb = $gMainProgressBar')

limit = 1000000


cmds.progressBar(gMainProgressBar, edit=True, beginProgress=True, isInterruptable=True, status="test", maxValue=limit)

for i in range(limit):
    if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True):
        break

    cmds.progressBar(gMainProgressBar, edit=True, step=1)

cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
