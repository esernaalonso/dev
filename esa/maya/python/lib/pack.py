#######################################
# imports

import os
import ntpath
import shutil
import re

import esa.maya.python.lib.main as main
import esa.maya.python.lib.inspector as inspector

reload(main)
reload(inspector)

#######################################
# functionality

def getPackFolder(pyFile):
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/modules/pack/" + os.path.splitext(ntpath.basename(pyFile))[0]

def packPyFileToModuleRecursive(pyFile, packFolder=None, searchScripts=[], mainFile=False):
    packedFiles = []

    if packFolder is None:
        packFolder = getPackFolder(pyFile)

    if len(searchScripts) == 0:
        searchScripts = main.getLibs() + main.getScripts() + main.getTools()

    # if file exist and is in search scripts process it
    if os.path.exists(pyFile) and pyFile in searchScripts:

        # open the file and read all the lines
        with open(pyFile, "r") as f:
            fileData = f.read()
            f.seek(0, 0)
            fileLines = f.readlines()

            packImportHead = os.path.basename(os.path.normpath(packFolder))
            packImportHead = packImportHead #+ ".scripts." + packImportHead

            # get all the import statements to substitute them for the new packed ones
            pyFileImports = inspector.getPyFileImports(pyFile)
            for importLine in pyFileImports:
                # we only need the last import module file to know if it is in the searchScripts
                imports = re.sub("from .* import ", "", importLine)
                imports = re.sub("import ", "", imports)
                imports = re.sub(" as .*", "", imports)
                imports = imports.replace(" ", "")

                # could be more than one import in each line, so we split it and loop them
                lineImports = imports.split(",")
                for singleImport in lineImports:
                    # could be a module.submodule.subsubmodule import, in that case we only need the last one to check if it is in the searchScripts
                    singleImportParts = singleImport.split(".")
                    if len(singleImportParts) > 0:
                        lastImport = singleImportParts[len(singleImportParts) - 1]

                    # adds the py extension to the end to search the script in the searchScripts
                    lastImportPy = lastImport + ".py"

                    # search the import in the searchScripts and if exists packs that file and replace the current import
                    importFile = [s for s in searchScripts if lastImportPy in s]
                    if len(importFile) > 0:
                        packedFiles += packPyFileToModuleRecursive(importFile[0], packFolder=packFolder, searchScripts=searchScripts)

                        if (importLine + "\n") in fileLines:
                            index = fileLines.index(importLine + "\n")

                            newImport = importLine.replace((singleImport.replace(lastImport, "")), (packImportHead + "."))
                            fileData = fileData.replace(importLine, newImport)

            packedPyFile = packFolder + "/" + os.path.splitext(ntpath.basename(pyFile))[0] + ".py"
            if mainFile:
                packedPyFile = packedPyFile.replace(".py", "Launcher.py")

            with open(packedPyFile, 'w') as fout:
                fout.write(fileData)
                packedFiles.append(packedPyFile)

            # print packedPyFile

    return packedFiles

def packUIfiles(packedPyFiles, packFolder):
    packedUIfiles = []

    uiFiles = main.getUIfiles()
    for uiFile in uiFiles:
        uiBaseNamePyBrother = os.path.splitext(ntpath.basename(uiFile))[0] + ".py"
        for pf in packedPyFiles:
            if uiBaseNamePyBrother in pf.replace("Launcher", ""):
                packedUIfile = packFolder + "/" + os.path.splitext(ntpath.basename(uiFile))[0] + ".ui"
                if "Launcher" in pf:
                    packedUIfile = packedUIfile.replace(".ui", "Launcher.ui")

                with open(uiFile, "r") as f:
                    fileData = f.read()
                    with open(packedUIfile, 'w') as fout:
                        fout.write(fileData)
                        packedUIfiles.append(packedUIfile)

    return packedUIfiles

def packDependentFiles(packedPyFiles, packFolder):
    packedDepFiles = []

    depFiles = main.getNonPyFiles()

    for packedFile in packedPyFiles:
        with open(packedFile, "r") as fpacked:
            packedFileData = fpacked.read()

            for depFile in depFiles:
                depFileName = ntpath.basename(depFile)
                if depFileName in packedFileData:
                    with open(depFile, "r") as fread:
                        depFileData = fread.read()
                        packedDepFile = packFolder + "/" + depFileName
                        with open(packedDepFile, 'w') as fout:
                            fout.write(depFileData)
                            packedDepFiles.append(packedDepFile)

    return packedDepFiles

def createPackPluginFile(pluginPyFile):
    pluginTemplateFile = os.path.dirname(__file__) + "/pluginTemplate.py"
    print pluginTemplateFile

    with open(pluginTemplateFile, "r") as fread:
        fileData = fread.read()
        fileData = fileData.replace("<pluginName>", os.path.splitext(ntpath.basename(pluginPyFile))[0])
        with open(pluginPyFile, 'w') as fout:
            fout.write(fileData)

def packPyFileToModule(pyFile, packFolder=None, searchScripts=[], removePrevious=False):
    print("\nSearching -> " + pyFile)

    if len(searchScripts) == 0:
        searchScripts = main.getLibs() + main.getScripts() + main.getTools()

    if os.path.exists(pyFile) and pyFile in searchScripts:
        print ("Found in scripts list -> " + pyFile)

        packName = os.path.splitext(ntpath.basename(pyFile))[0]

        # first of all we need a pack folder. if not provided is calculated by default.
        if not packFolder:
            packFolder = getPackFolder(pyFile)
            print ("Pack folder not provided. Using default -> " + packFolder)

        packFolderScripts = packFolder + "/" + packName + "/scripts/" + packName

        # if a clean pack is needed, the old one is deleted
        if os.path.exists(packFolder) and removePrevious:
            shutil.rmtree(packFolder)

        # if the packFolder doesn't exist, is created
        if not os.path.exists(packFolder) or not os.path.exists(packFolderScripts):
            os.makedirs(packFolderScripts)
            print ("Pack folder creation -> " + packFolderScripts)

        # if everything is ok the packing starts
        if os.path.exists(packFolderScripts):
            print ("Pack folder exists -> " + packFolderScripts)

            # packs the .py files
            print "Packing .py files..."
            packedPyFiles = packPyFileToModuleRecursive(pyFile, packFolder=packFolderScripts, searchScripts=searchScripts, mainFile=True)
            print "Packed .py files:"
            for pf in packedPyFiles: print ("    " + pf)

            # packs the .ui files
            print "Packing .ui files..."
            packedUIfiles = packUIfiles(packedPyFiles, packFolderScripts)
            print "Packed .ui files:"
            for puf in packedUIfiles: print ("    " + puf)

            # packs all other possible dependent files
            print "Packing other dependent files..."
            packedDepFiles = packDependentFiles(packedPyFiles, packFolderScripts)
            print "Packed dependent files:"
            for pdep in packedDepFiles: print ("    " + pdep)

            # creates the pack init file for the pack and for the scripts folder

            # packInitFile = packFolder + "/" + packName + "/__init__.py"
            # with open(packInitFile, 'w') as fout: fout.write("")
            # print ("Pack __init__ file creation -> " + packInitFile)

            packScriptsInitFile = packFolderScripts + "/__init__.py"
            with open(packScriptsInitFile, 'w') as fout: fout.write("")
            print ("Pack scripts __init__ file creation -> " + packScriptsInitFile)

            # the pack needs a mod file to be read by maya at open
            modFile = packFolder + "/" + packName + ".mod"
            print ("Creating pack mod file...")
            with open(modFile, 'w') as fout:
                fout.write("+ " + packName + " 1.0.0 ../modules/pack/" + packName + "\n")
            print ("Created pack mod file -> " + modFile)

            # creates the plugin folder for the pack and the plugin to be read by maya

            packFolderPlugins = packFolder + "/" + packName + "/plug-ins"
            if not os.path.exists(packFolderPlugins):
                os.makedirs(packFolderPlugins)
                print ("Pack plug-ins folder creation -> " + packFolderPlugins)

            if os.path.exists(packFolderPlugins):
                pluginFile = packFolderPlugins + "/" + packName + ".py"
                print ("Creating pack plugin file...")
                createPackPluginFile(pluginFile)
                print ("Created pack plugin file -> " + pluginFile)
    else:
        print("Not found in scripts list -> " + pyFile)

def getPyFileCompiledString(pyFile, searchScripts=[]):
    compiledString = ""

    packName = os.path.splitext(ntpath.basename(pyFile))[0]

    if len(searchScripts) == 0:
        searchScripts = main.getLibs() + main.getScripts() + main.getTools()

    # imports section
    compiledString += "#######################################\n"
    compiledString += "# imports\n\n"

    # gets all non dependent imports and add them to the future string
    noDepImports = inspector.getPyFileNonDependentImports(pyFile, recursive=True, searchScripts=searchScripts)
    noDepImports.sort()
    for imp in noDepImports:
        compiledString += imp + "\n"

    # gets all file dependent imports. They are needed to make replacements later
    depImports = inspector.getPyFileDependentImports(pyFile, recursive=True, searchScripts=searchScripts, nameOnly=True)

    # get all file and dependent files first level definitions to include them if they are used
    # only definitions that are used should be added
    definitions = inspector.getPyFileDefinitions(pyFile, level=0, recursive=True, searchScripts=searchScripts, ignoreNotUsed=False)
    definitionsNames = inspector.getPyFileDefinitions(pyFile, level=0, recursive=True, searchScripts=searchScripts, ignoreNotUsed=False, onlyNames=True)

    # get all file and dependent files first level classes to include them if they are used
    classes = inspector.getPyFileClasses(pyFile, level=0, recursive=True, searchScripts=searchScripts, ignoreNotUsed=False)
    classesNames = inspector.getPyFileClasses(pyFile, level=0, recursive=True, searchScripts=searchScripts, ignoreNotUsed=False, onlyNames=True)

    # now is time to discard not used defs and classes and keep only the dependent ones
    usedDefinitions = []
    usedDefinitionsNames = []
    with open(pyFile, "r") as f:
        fileData = f.read()
        definitionsParents = inspector.getPyFileBlocksParents(definitionsNames, (definitions + classes), fileData, lastAncestors=True)
        # print len(definitionsNames)
        # print len(definitions)
        # print len(definitionsParents)
        for i in range(len(definitions)):
            if "pyFile" in definitionsParents[i]:
                # print definitionsNames[i]
                # print definitionsParents[i]
                usedDefinitions.append(definitions[i])
                usedDefinitionsNames.append(definitionsNames[i])

    # for i in range(len(definitions)):
    #     print definitionsNames[i]

    # definitions section
    compiledString += "\n#######################################\n"
    compiledString += "# definitions\n\n"

    # definitions process. Adds the definitions
    for i in range(len(usedDefinitions)):
        compiledString += usedDefinitions[i] + "\n"

    # classes section
    compiledString += "\n#######################################\n"
    compiledString += "# classes\n\n"

    # classes process. Adds the definitions
    for i in range(len(classes)):
        compiledString += classes[i] + "\n"

    # after adding the definitions and classes, calls must be updated from module.definition() to definition()
    for i in range(len(definitionsNames)):
        regx = re.compile(("(.*\." + definitionsNames[i] + "\(.*)"), re.MULTILINE)
        matches = regx.findall(compiledString)
        if len(matches) > 0:
            for match in matches:
                regx2 = re.compile((".*(?:\s)(.*\." + definitionsNames[i] + ")\(.*"), re.MULTILINE)
                defCallMatches = regx2.findall(match)
                defCallSplit = defCallMatches[len(defCallMatches) - 1].split("(")
                defCall = defCallSplit[len(defCallSplit) - 1]
                # print defCall
                # defCallParts = defCall.split(".")
                defCallParts = re.split("\.|=", defCall)
                defCallLib = defCallParts[len(defCallParts) - 2]
                defCallDef = defCallParts[len(defCallParts) - 1]
                # print defCallLib
                # print defCallDef
                if defCallLib in depImports:
                    compiledString = compiledString.replace((defCallLib + "." + defCallDef), defCallDef)

    # adds the execution string
    compiledString += "\n#######################################\n"
    compiledString += "# execution\n"
    compiledString += 'if __name__ == "__main__": ' + packName + 'Run()'

    return compiledString

def packPyFile(pyFile, packFolder=None, searchScripts=[], removePrevious=False):
    print("\nSearching -> " + pyFile)

    if len(searchScripts) == 0:
        searchScripts = main.getLibs() + main.getScripts() + main.getTools()

    if os.path.exists(pyFile) and pyFile in searchScripts:
        print ("Found in scripts list -> " + pyFile)

        packName = os.path.splitext(ntpath.basename(pyFile))[0]

        # first of all we need a pack folder. if not provided is calculated by default.
        if not packFolder:
            packFolder = getPackFolder(pyFile)
            print ("Pack folder not provided. Using default -> " + packFolder)

        # if a clean pack is needed, the old one is deleted
        if os.path.exists(packFolder) and removePrevious:
            shutil.rmtree(packFolder)

        # if the packFolder doesn't exist, is created
        if not os.path.exists(packFolder):
            os.makedirs(packFolder)
            print ("Pack folder creation -> " + packFolder)

        # if everything is ok the packing starts
        if os.path.exists(packFolder):
            print ("Pack folder exists -> " + packFolder)

            packFile = packFolder + "/" + packName + ".py"
            print ("Compiling file content -> " + packFile)
            compiledString = getPyFileCompiledString(pyFile, searchScripts=searchScripts)

            print ("Writing file content -> " + packFile)
            with open(packFile, 'w') as fout:
                fout.write(compiledString)

            depFiles = [pyFile] + inspector.getPyFileDependentPyFiles(pyFile, recursive=True, searchScripts=searchScripts)

            print ("Packing UI files for -> " + packFile)
            packUIfiles(depFiles, packFolder)

            print ("Packing dependent files for -> " + packFile)
            packDependentFiles(depFiles, packFolder)

            packInitFile = packFolder + "/" + "/__init__.py"
            print ("Creating __init__ file -> " + packInitFile)
            with open(packInitFile, 'w') as fout: fout.write("")

            print ("Process Finished -> " + packFile)
    else:
        print("Not found in scripts list -> " + pyFile)

def test():
    # testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/renamer.py"
    # testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/bakeACPdynamics.py"
    # testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/projectionManager.py"
    # testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/playblastToGIF.py"
    # testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/templateToolStd.py"
    # testFile = "P:\\dev\\esa\\maya\\python\\tool\\anim\\projectionManager.py"
    # testFile = "P:\\dev\\esa\\maya\\python\\tool\\misc\\renamer.py"
    # testFile = "P:\\dev\\esa\\maya\\python\\tool\\template\\templateToolStd.py"
    # testFile = "P:\\dev\\esa\\maya\\python\\tool\\template\\templateToolDock.py"
    testFile = "P:\\dev\\esa\\maya\\python\\tool\\template\\templateToolStdUI.py"

    # packPyFileToModule(testFile, removePrevious=True)
    packPyFile(testFile, removePrevious=True)

#######################################
# execution

if __name__ == "__main__":
    test()
    pass