#######################################
# imports

import re
import sys
import inspect

import esa.maya.python.lib.main as main

reload(main)

#######################################
# functionality\

def isModFunction(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod

def getModFunctions(mod):
    return [func.__name__ for func in mod.__dict__.itervalues()
            if isModFunction(mod, func)]

def getPyFileImports(pyFile):
	pyFileImports = []

	with open(pyFile, "r") as f:
		data = f.read()
		f.close()

		regx = re.compile('(.*import .*)', re.MULTILINE)
		matches = regx.findall(data)
		if len(matches) > 0:
			for match in matches:
				if " re." not in match:
					pyFileImports.append(match)

	return pyFileImports

def getPyFileNonDependentImports(pyFile, recursive=False, searchScripts=[], nameOnly=False, recursiveExploredFiles=[]):
	nonDependentImports = []

	if len(searchScripts) == 0:
		searchScripts = main.getLibs() + main.getScripts() + main.getTools()

	importLines = getPyFileImports(pyFile)

	for importLine in importLines:
		importContent = re.sub(".*import (.*)", r"\1", importLine)
		importContent = re.sub("(.*) as.*", r"\1", importContent)
		singleImports = importContent.split(", ")

		for singleImport in singleImports:
			singleImport = singleImport.split(".")
			singleImport = singleImport[len(singleImport) - 1]
			singleImport += ".py"

			found = False
			for searchScript in searchScripts:
				if (singleImport in searchScript) and (searchScript not in recursiveExploredFiles):
					found = True
					if recursive:
						recursiveNonDependents = getPyFileNonDependentImports(searchScript, recursive=recursive, searchScripts=searchScripts, recursiveExploredFiles=(recursiveExploredFiles + [searchScript]))
						for rd in recursiveNonDependents:
							if rd not in nonDependentImports:
								nonDependentImports.append(rd)

			if not found and importLine not in nonDependentImports:
				nonDependentImports.append(importLine)

	if nameOnly:
		defNonDepImports = []
		for i in range(len(nonDependentImports)):
			if " as " in nonDependentImports[i]:
				importParts = nonDependentImports[i].split(" ")
				defNonDepImports.append(importParts[len(importParts) - 1])
			else:
				importContent = re.sub(".*import (.*)", r"\1", nonDependentImports[i])
				singleImports = importContent.split(", ")
				for simp in singleImports:
					defNonDepImports.append(simp)
		nonDependentImports = defNonDepImports

	return nonDependentImports

def getPyFileDependentImports(pyFile, recursive=False, searchScripts=[], nameOnly=False, recursiveExploredFiles=[]):
	dependentImports = []

	if len(searchScripts) == 0:
		searchScripts = main.getLibs() + main.getScripts() + main.getTools()

	importLines = getPyFileImports(pyFile)

	for importLine in importLines:
		importContent = re.sub(".*import (.*)", r"\1", importLine)
		importContent = re.sub("(.*) as.*", r"\1", importContent)
		singleImports = importContent.split(", ")

		for singleImport in singleImports:
			singleImport = singleImport.split(".")
			singleImport = singleImport[len(singleImport) - 1]
			singleImport += ".py"

			for searchScript in searchScripts:
				if (singleImport in searchScript) and (searchScript not in recursiveExploredFiles):
					if recursive:
						recursiveDependents = getPyFileDependentImports(searchScript, recursive=recursive, searchScripts=searchScripts, recursiveExploredFiles=(recursiveExploredFiles + [searchScript]))
						for rd in recursiveDependents:
							if rd not in dependentImports:
								dependentImports.append(rd)

					if importLine not in dependentImports:
						dependentImports.append(importLine)

	if nameOnly:
		defDepImports = []
		for i in range(len(dependentImports)):
			if " as " in dependentImports[i]:
				importParts = dependentImports[i].split(" ")
				defDepImports.append(importParts[len(importParts) - 1])
			else:
				importContent = re.sub(".*import (.*)", r"\1", dependentImports[i])
				singleImports = importContent.split(", ")
				for simp in singleImports:
					defDepImports.append(simp)
		dependentImports = defDepImports

	return dependentImports

def getPyFileDependentPyFiles(pyFile, recursive=False, searchScripts=[], recursiveExploredFiles=[]):
	dependentFiles = []

	if len(searchScripts) == 0:
		searchScripts = main.getLibs() + main.getScripts() + main.getTools()

	depImports = getPyFileDependentImports(pyFile, searchScripts=searchScripts)
	for di in depImports:
		importContent = re.sub(".*import (.*)", r"\1", di)
		importContent = re.sub("(.*) as.*", r"\1", importContent)
		singleImports = importContent.split(", ")

		for singleImport in singleImports:
			singleImport = singleImport.split(".")
			singleImport = singleImport[len(singleImport) - 1]
			singleImport += ".py"

			for searchScript in searchScripts:
				if (singleImport in searchScript) and (searchScript not in recursiveExploredFiles):
					if recursive:
						recursiveDependents = getPyFileDependentPyFiles(searchScript, recursive=recursive, searchScripts=searchScripts, recursiveExploredFiles=(recursiveExploredFiles + [searchScript]))
						for rd in recursiveDependents:
							if rd not in dependentFiles:
								dependentFiles.append(rd)

					if searchScript not in dependentFiles:
						dependentFiles.append(searchScript)

	return dependentFiles

def getBlockName(block):
	return re.split("\W+", block)[1]

def getPyFileBlockParents(blockName, blocks, pyFileStringData, lastAncestors=False, currentBlockParents=[]):
	blockParents = []

	# print "- - - - - - - - - - - - - - - - - - - - - - - -"
	# print blockName

	if (blockName + "(") in pyFileStringData:
		blockParents.append("pyFile")

	for j in range(len(blocks)):
		if (blockName + "(") in blocks[j]:
			currentBlockName = getBlockName(blocks[j])

	# 		# print blocksNames[j]
	# 		# print "-----------"
			if (currentBlockName != blockName) and (currentBlockName not in currentBlockParents):
				if not lastAncestors:
					blockParents.append(blocksNames[j])
				else:
					supParents = getPyFileBlockParents(currentBlockName, blocks, pyFileStringData, lastAncestors=True, currentBlockParents=(blockParents + [blockName]))
					for p in supParents:
						if p not in blockParents:
							blockParents.append(p)

	# print blockParents
	# print "-----------------------------------------------------------"

	return blockParents

def getPyFileBlocksParents(blocksNames, blocks, pyFileStringData, lastAncestors=False):
	parentsNames = []

	if len(blocksNames) > 0 and len(blocks) > 0:
		for i in range(len(blocksNames)):
			blockParents = getPyFileBlockParents(blocksNames[i], blocks, pyFileStringData, lastAncestors=lastAncestors)
			parentsNames.append(blockParents)

	return parentsNames

def getPyFileBlocks(pyFile, blockTag, level=0, recursive=False, searchScripts=[], ignoreNotUsed=False, onlyNames=False, recursiveExploredFiles=[]):
	pyFileBlocks = []

	with open(pyFile, "r") as f:
		fileData = f.read()
		f.seek(0, 0)
		fileLines = f.readlines()

		if recursive:
			if len(searchScripts) == 0:
				searchScripts = main.getLibs() + main.getScripts() + main.getTools()

			depFiles = getPyFileDependentPyFiles(pyFile, searchScripts=searchScripts)
			for df in depFiles:
				if df not in recursiveExploredFiles:
					subFileBlocks = getPyFileBlocks(df, blockTag, level=level, recursive=True, searchScripts=searchScripts, ignoreNotUsed=ignoreNotUsed, onlyNames=False, recursiveExploredFiles = (recursiveExploredFiles + [df]))

					if not ignoreNotUsed:
						for sfb in subFileBlocks:
							if sfb not in pyFileBlocks:
								pyFileBlocks.append(sfb)
					else:
						subFileBlocksNames = getPyFileBlocks(df, blockTag, level=level, recursive=True, searchScripts=searchScripts, ignoreNotUsed=ignoreNotUsed, onlyNames=True, recursiveExploredFiles = (recursiveExploredFiles + [df]))
						subFileBlocksAncestors = getPyFileBlocksParents(subFileBlocksNames, subFileBlocks, fileData, lastAncestors=True)

						# print len(subFileBlocks)
						# print len(subFileBlocksNames)
						# print len(subFileBlocksAncestors)
						# print "------------------------"

						# for i in range(len(subFileBlocksNames)):
						# 	print pyFile
						# 	print subFileBlocksNames[i]
						# 	print subFileBlocksAncestors[i]
						# 	print ("pyFile" in subFileBlocksAncestors[i])
						# 	print "-------------------------------"

						for i in range(len(subFileBlocks)):
							if "pyFile" in subFileBlocksAncestors[i]:
								pyFileBlocks.append(subFileBlocks[i])

		state = "searchTag"
		currentCompilation = ""

		for line in fileLines:
			jumpNextLine = False

			for i in range(level):
				if line.startswith("	"):
					line = line[1:]
				elif line.startswith("    "):
					line = line[4:]
				else:
					if state == "searchTagContent":
						if line != "\n":
							state = "searchTag"
							pyFileBlocks.append(currentCompilation)
							currentCompilation = ""
							jumpNextLine = True

			if jumpNextLine: continue

			if state == "searchTagContent":
				if line.startswith("	") or line.startswith("    ") or line == "\n":
					currentCompilation += line
				else:
					state = "searchTag"
					pyFileBlocks.append(currentCompilation)
					currentCompilation = ""

			if state == "searchTag":
				if line.startswith(blockTag):
					currentCompilation += line

					state = "searchTagContent"
					jumpNextLine = True

			if jumpNextLine: continue

	if onlyNames:
		for i in range(len(pyFileBlocks)):
			pyFileBlocks[i] = getBlockName(pyFileBlocks[i])

	return pyFileBlocks

def getPyFileDefinitions(pyFile, level=0, recursive=False, searchScripts=[], ignoreNotUsed=False, onlyNames=False):
	return getPyFileBlocks(pyFile, "def", level=level, recursive=recursive, searchScripts=searchScripts, ignoreNotUsed=ignoreNotUsed, onlyNames=onlyNames)

def getPyFileClasses(pyFile, level=0, recursive=False, searchScripts=[], ignoreNotUsed=False, onlyNames=False):
	return getPyFileBlocks(pyFile, "class", level=level, recursive=recursive, searchScripts=searchScripts, ignoreNotUsed=ignoreNotUsed, onlyNames=onlyNames)

def test():
	# testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/lib/rig.py"
	# testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/bakeACPdynamics.py"
	testFile = "/usr/people/eduardo-a/dev/toolCage/toolCage/tool/projectionManager.py"

	# imports = getPyFileImports(testFile)
	# for imp in imports: print imp

	# imports = getPyFileDependentImports(testFile, recursive=True, nameOnly=True)
	# print "-------------------"
	# for imp in imports: print imp

	# imports = getPyFileNonDependentImports(testFile, recursive=True, nameOnly=True)
	# print "-------------------"
	# for imp in imports: print imp

	# defs = getPyFileDefinitions(testFile, level=0, recursive=True, onlyNames=True, ignoreNotUsed=True)
	# defs2 = getPyFileDefinitions(testFile, level=0, recursive=True, onlyNames=False, ignoreNotUsed=True)
	# defs = getPyFileDefinitions(testFile, level=0, recursive=True, onlyNames=True, ignoreNotUsed=False)
	# print "\n\n- - - - - - - - - - - - - - - - - - - - - - - - - -"
	# for i in range(len(defs)):
	# 	print defs[i]
	# 	print defs2[i]
	# 	print "- - - - - - - - - - - - - - - - - - - - - - - - - -"
	# print (len(defs))

	# classes = getPyFileClasses(testFile, level=0, recursive=True, onlyNames=True)
	# for c in classes:
	# 	print c
	# 	print "- - - - - - - - - - - - - - - - - - - - - - - - - -"
	# print (len(classes))
	pass

#######################################
# execution

if __name__ == "__main__":
	test()
	pass