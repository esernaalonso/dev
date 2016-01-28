#######################################
# imports

import os
import sys
# import shiboken
import ntpath
# import importlib
import psutil

from PySide import QtCore, QtGui
# from shiboken import wrapInstance


#######################################
# functionality


def isToolOpened(toolName):
    for proc in psutil.process_iter():
        if "python.exe" in proc.name():
            process_toolName = os.path.splitext(os.path.basename(proc.cmdline()[-1:][0]))[0]
            if process_toolName == toolName:
                return True

    return False


def closeTool(toolName):
    for proc in psutil.process_iter():
        if "python.exe" in proc.name():
            process_toolName = os.path.splitext(os.path.basename(proc.cmdline()[-1:][0]))[0]
            if process_toolName == toolName:

                children = proc.children(recursive=True)
                for child in children:
                    child.kill()
                psutil.wait_procs(children, timeout=5)

                proc.kill()

    return True
#
# def getTool(toolName):
#     mayaWindow = getMayaWindow()
#     return mayaWindow.findChild(QtGui.QDialog, toolName)
#
# def openTool(toolName, module=None):
#     if module == None: module = mayaWindow.findChild(QtGui.QDialog, toolName)
#     if module == None:
#         importStatement = main.getPyFileFullImportName(sToolFileName)
#         module = importlib.import_module(importStatement)
#
#     toolFunctions = inspector.getModFunctions(module)
#     for tf in toolFunctions:
#         if (tf == "run") or (tf.lower() == (toolName.lower() + "run")):
#             getattr(module, tf)()
#
# def executeScript(scriptName, module=None):
#     if module == None: module = mayaWindow.findChild(QtGui.QDialog, scriptName)
#     if module == None:
#         importStatement = main.getPyFileFullImportName(sToolFileName)
#         module = importlib.import_module(importStatement)
#
#     scriptFunctions = inspector.getModFunctions(module)
#     for sf in scriptFunctions:
#         if (sf == "run") or (sf.lower() == (scriptName.lower() + "run")):
#             getattr(module, sf)()
#
# def getSelfToolName(file):
#     return ntpath.basename(file).replace(".py", "")

#######################################
# execution

if __name__ == "__main__":
    # print "test operations"
    if (isToolOpened("templateToolStdUI")):
        closeTool("templateToolStdUI")
    # print (isToolOpened("templateToolDock"))
    # print (importModule("templateToolStd"))
    pass
