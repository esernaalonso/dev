#######################################
# imports

import os
import shutil

from distutils import dir_util
from glob import glob

#######################################
# functionality

def getImmediateSubfolders(p_sDir):
	return [os.path.join(p_sDir, name) for name in os.listdir(p_sDir) if (os.path.isdir(os.path.join(p_sDir, name)) and (name != ".git") and (name != ".svn"))]

def getImmediateFolderFiles(p_sDir):
	return [os.path.join(p_sDir, name) for name in os.listdir(p_sDir) if (os.path.isfile(os.path.join(p_sDir, name)))]

def getRecursiveSubdfolders(p_sDir):
	p_recSubfolders = [p_sDir]
	p_subfolders = getImmediateSubfolders(p_sDir)

	for p in p_subfolders:
		# p_recSubfolders.append(p)
		p_recSubfolders += getRecursiveSubdfolders(p)

	return p_recSubfolders

def copyPathRecursive(originDir, destinDir):
	for root, dirs, files in os.walk(originDir):
	    for item in files:
	        src_path = os.path.join(root, item)
	        dst_path = os.path.join(destinDir, src_path.replace(originDir, ""))
	        if os.path.exists(dst_path):
	            if os.stat(src_path).st_mtime > os.stat(dst_path).st_mtime:
	                shutil.copy2(src_path, dst_path)
	        else:
	            shutil.copy2(src_path, dst_path)
	    for item in dirs:
	        src_path = os.path.join(root, item)
	        dst_path = os.path.join(destinDir, src_path.replace(originDir, ""))
	        if not os.path.exists(dst_path):
	            os.mkdir(dst_path)

def removePathRecursive(destinDir):
	if os.path.isdir(destinDir):
	 	dir_util.remove_tree(destinDir)

def removePycFilesRecursive(initPath):
	for pth in getRecursiveSubdfolders(initPath):
		for pycFile in glob(pth + "/*.pyc"):
   			os.remove(pycFile)

#######################################
# execution
 
if __name__ == "__main__":
	# print "test operations"
	pass