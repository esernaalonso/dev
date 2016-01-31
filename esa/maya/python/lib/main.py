#######################################
# imports

import os
import sys
import ntpath
import importlib
import re
import itertools

# import utils
import esa.maya.python.lib.io as io
import esa.maya.python.lib.permissions as permissions

# reload(utils)
reload(io)
reload(permissions)

#######################################
# functionality

# returns the .py categories (this is teh folder paths names after "toolCage" till fileName not included)
def getPyFileCategoryTree(p_sFile):
    lCategories = p_sFile.split(os.path.sep)
    lCategories.remove(lCategories[len(lCategories)-1])
    itertools.groupby(lCategories, lambda sep: sep == "python")
    lCategories = [list(group) for j, group in itertools.groupby(lCategories, lambda sep: sep == "python") if not j][1]

    return lCategories

# returns the .py running type (plugins, tool, script or lib)
def getPyFileType(p_sFile):
    sType = "unKnown"

    thisFile = os.path.splitext(ntpath.basename(__file__))[0].lower()
    fileName = os.path.splitext(ntpath.basename(p_sFile))[0].lower()
    p_sFilePath = p_sFile.replace(".pyc", ".py")

    if os.path.exists(p_sFilePath):
        f = open(p_sFilePath, "r")
        if f is not None:
            data = f.read()

            sType = "tool"
            if (not "def close():" in data.lower()) and (not ("def " + fileName + "close():") in data.lower()) or (thisFile == fileName): sType = "script"
            if (not "def run():" in data.lower()) and (not ("def " + fileName + "run():") in data.lower()) or (thisFile == fileName): sType = "lib"
            if ("def uninitializePlugin(mobject):" in data) and (thisFile != fileName): sType = "plugin"

            f.close()

    return sType

# returns the .py full imported statement name (example: "esa.maya.python.lib.main")
def getPyFileFullImportName(p_sFile):
    importStatement = ""

    p_sFilePath = p_sFile.replace(".pyc", "")
    p_sFilePath = p_sFilePath.replace(".py", "")

    pathParts = re.split("python", p_sFilePath)
    print pathParts
    if len(pathParts) > 1:
        importStatement = "esa.maya.python" + pathParts[1].replace(os.path.sep, ".")

    print importStatement

    return importStatement

# returns the .py permissions type (developer, artist)
def getPyFilePermissionLevel(p_sFile):
    permissionLevel = None

    p_sFilePath = p_sFile.replace(".pyc", ".py")

    if os.path.exists(p_sFilePath):
        f = open(p_sFilePath, "r")
        if f is not None:
            data = f.read()

            regx = re.compile('.*?permission = "(.*)"', re.MULTILINE)
            matches = regx.search(data).groups()
            if len(matches) > 0:
                permissionLevel = matches[0]

            f.close()

    return permissionLevel

def getUIfiles(p_sInitPath=None, p_bRecursive=True):
    uiFiles = []

    if p_sInitPath is None:
        p_sInitPath = os.path.dirname(os.path.dirname(__file__))

    sDirFiles = os.listdir(p_sInitPath)

    for sFile in sDirFiles:
        if (os.path.splitext(sFile)[1] == ".ui"):
            uiFiles.append(p_sInitPath + os.path.sep + sFile)

    if p_bRecursive:
        sSubdirs = io.getImmediateSubfolders(p_sInitPath)
        for sPath in sSubdirs:
            uiSubFiles = getUIfiles(p_sInitPath=sPath, p_bRecursive=p_bRecursive)
            uiFiles.extend(uiSubFiles)

    return uiFiles

def getNonPyFiles(p_sInitPath=None, p_bRecursive=True):
    nonPyFiles = []
    ignoreTypes = [".py", ".pyc", ".ui"]

    if p_sInitPath is None:
        p_sInitPath = os.path.dirname(os.path.dirname(__file__))

    sDirFiles = os.listdir(p_sInitPath)

    for sFile in sDirFiles:
        if os.path.isfile(os.path.join(p_sInitPath, sFile)):
            fileExt = os.path.splitext(sFile)[1]
            if fileExt not in ignoreTypes:
                nonPyFiles.append(p_sInitPath + os.path.sep + sFile)

    if p_bRecursive:
        sSubdirs = io.getImmediateSubfolders(p_sInitPath)
        for sPath in sSubdirs:
            uiSubFiles = getNonPyFiles(p_sInitPath=sPath, p_bRecursive=p_bRecursive)
            nonPyFiles.extend(uiSubFiles)

    return nonPyFiles

# returns all the py files in the specified folder and subdirectories recursively if indicated
def getPyFilesByType(p_sInitPath=None, p_sType="", p_bRecursive=True, ignorePermissions=False):
    lPyFiles = []

    if p_sInitPath is None:
        p_sInitPath = os.path.dirname(os.path.dirname(__file__))

    sDirFiles = os.listdir(p_sInitPath)

    for sFile in sDirFiles:
        if (os.path.splitext(sFile)[1] == ".py"):
            sType = getPyFileType(p_sInitPath + os.path.sep + sFile)
            if p_sType == "" or p_sType == sType: lPyFiles.append(p_sInitPath + os.path.sep + sFile)

    # removes the elements not allowed by permissions if necessary
    if not ignorePermissions:
        permissionLevel = permissions.getUserPermissionLevel()
        if permissionLevel != "developer":
            for i in range((len(lPyFiles) - 1), -1, -1):
                perLevel = getPyFilePermissionLevel(lPyFiles[i])
                if perLevel != permissionLevel:
                    lPyFiles.remove(lPyFiles[i])

    if p_bRecursive:
        sSubdirs = io.getImmediateSubfolders(p_sInitPath)
        for sPath in sSubdirs:
            lPySubFiles = getPyFilesByType(p_sInitPath=sPath, p_sType=p_sType, p_bRecursive=p_bRecursive, ignorePermissions=ignorePermissions)
            lPyFiles.extend(lPySubFiles)

    return lPyFiles

# returns all the lib files in the specified folder and subdirectories recursively if indicated
def getLibs(p_sInitPath=None, p_bRecursive=True, ignorePermissions=False):
    return (getPyFilesByType(p_sInitPath=p_sInitPath, p_sType="lib", p_bRecursive=p_bRecursive, ignorePermissions=ignorePermissions))

# returns all the tool files in the specified folder and subdirectories recursively if indicated
def getTools(p_sInitPath=None, p_bRecursive=True, ignorePermissions=False):
    return (getPyFilesByType(p_sInitPath=p_sInitPath, p_sType="tool", p_bRecursive=p_bRecursive, ignorePermissions=ignorePermissions))

# returns all the script files in the specified folder and subdirectories recursively if indicated
def getScripts(p_sInitPath=None, p_bRecursive=True, ignorePermissions=False):
    return (getPyFilesByType(p_sInitPath=p_sInitPath, p_sType="script", p_bRecursive=p_bRecursive, ignorePermissions=ignorePermissions))

# returns all the plugin files in the specified folder and subdirectories recursively if indicated
def getPlugins(p_sInitPath=None, p_bRecursive=True):
    return (getPyFilesByType(p_sInitPath=p_sInitPath, p_sType="plugin", p_bRecursive=p_bRecursive))

#######################################
# execution

if __name__ == "__main__":
    # print (getLibs())
    # print (getTools())
    # print (getScripts())
    # print (getPlugins())
    # print (getNonPyFiles())
    print (getPyFileFullImportName("P:\\dev\\esa\\maya\\python\\lib\\main.py"))
    pass
