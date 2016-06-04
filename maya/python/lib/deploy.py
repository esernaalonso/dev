#######################################
# imports

import os
import shutil
import subprocess
import getpass
import socket
import signal

from glob import glob

import esa.maya.python.lib.io as io

reload(io)

#######################################
# functionality

def deployCurrentToolCageDev():
	# build the paths
	toolCageDevPath = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
	toolCageToolPath = toolCageDevPath.replace("dev", "tools")

	# removes previows deploy
	if os.path.exists(toolCageToolPath): shutil.rmtree(toolCageToolPath)

	# creates deploy directories
	os.makedirs(toolCageToolPath + "/")
	os.makedirs(toolCageToolPath + "/mod/")
	os.makedirs(toolCageToolPath + "/plug-ins/")
	os.makedirs(toolCageToolPath + "/toolCage/external/")
	os.makedirs(toolCageToolPath + "/toolCage/lib/")
	os.makedirs(toolCageToolPath + "/toolCage/script/")
	os.makedirs(toolCageToolPath + "/toolCage/tool/")

	# deploy
	io.copyPathRecursive((toolCageDevPath + "/mod/"), (toolCageToolPath + "/mod/"))
	io.copyPathRecursive((toolCageDevPath + "/plug-ins/"), (toolCageToolPath + "/plug-ins/"))
	io.copyPathRecursive((toolCageDevPath + "/toolCage/external/"), (toolCageToolPath + "/toolCage/external/"))
	io.copyPathRecursive((toolCageDevPath + "/toolCage/lib/"), (toolCageToolPath + "/toolCage/lib/"))
	io.copyPathRecursive((toolCageDevPath + "/toolCage/script/"), (toolCageToolPath + "/toolCage/script/"))
	io.copyPathRecursive((toolCageDevPath + "/toolCage/tool/"), (toolCageToolPath + "/toolCage/tool/"))

	# removes

	# dev plugins
	for pth in io.getRecursiveSubdfolders(toolCageToolPath + "/plug-ins"):
		for devPyFile in glob(pth + "/*Dev.py"):
			os.remove(devPyFile)

	# dev mods
	if os.path.exists(toolCageToolPath + "/mod/toolCageDevInit.mod"):
		os.remove(toolCageToolPath + "/mod/toolCageDevInit.mod")

	# removes pycFiles
	io.removePycFilesRecursive(toolCageToolPath)

def installModToUser(username, password=None):
	currentUser = getpass.getuser()
	currentUserFolder = "/usr/people/" + currentUser
	currentMachine = socket.gethostname().replace(".mpc.local", "")

	userMayaPath = "/usr/people/" + username + "/maya/2015-x64/"
	userModulesPath = "/usr/people/" + username + "/maya/2015-x64/modules/"
	
	originModFile = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "/mod/toolCageInit.mod"
	destModFile = userModulesPath + "toolCageInit.mod"

	# FOLDER: if modules path not exist, creates it
	if not os.path.isdir(userModulesPath) and os.path.isdir(userMayaPath):
		# if password, try to use mpcsu to create folder

		if password is not None:
			deployMkdirMpcsuFile = os.path.dirname(__file__) + "/deploy-installModToUser-mpcsu-mkdir.exp"
			deployMkdirMpcsuFileForUser = currentUserFolder + "/deploy-installModToUser-mpcsu-mkdir.exp"
			
			# duplicate the file and modify the content for the current execution
			replacements = {"_destUser_":username, "_currentUser_":currentUser, "_currentMachine_":currentMachine, "_password_":password}

			data = open(deployMkdirMpcsuFile).read()
			outfile = open(deployMkdirMpcsuFileForUser, 'w')

			for i in replacements.keys():
				data = data.replace(i, replacements[i])
			
			outfile.write(data)
			outfile.close()

			if os.path.exists(deployMkdirMpcsuFileForUser):
				p = subprocess.Popen(["expect", deployMkdirMpcsuFileForUser], stdout=subprocess.PIPE)
				output, err = p.communicate()
				os.remove(deployMkdirMpcsuFileForUser)

			print ("Folder modules created in user " + username + ": " + userModulesPath)
		else:
			# if not password, try to do it in the traditional way
			os.makedirs(userModulesPath)
			print ("Folder modules created in user " + username + ": " + userModulesPath)

	# FILE: Copy the .mod file to the user folder
	if os.path.isdir(userModulesPath) and os.path.exists(originModFile):
		if password is not None:
			# if password, try to use mpcsu to copy the file

			deployCpMpcsuFile = os.path.dirname(__file__) + "/deploy-installModToUser-mpcsu-cp.exp"
			deployCpMpcsuFileForUser = currentUserFolder + "/deploy-installModToUser-mpcsu-cp.exp"
			
			# duplicate the file and modify the content for the current execution
			replacements = {"_destUser_":username, "_currentUser_":currentUser, "_currentMachine_":currentMachine, "_password_":password}

			data = open(deployCpMpcsuFile).read()
			outfile = open(deployCpMpcsuFileForUser, 'w')

			for i in replacements.keys():
				data = data.replace(i, replacements[i])
				
			outfile.write(data)
			outfile.close()

			if os.path.exists(deployCpMpcsuFileForUser):
				p2 = subprocess.Popen(["expect", deployCpMpcsuFileForUser], stdout=subprocess.PIPE)
				output, err = p2.communicate()
				
				os.remove(deployCpMpcsuFileForUser)
		else:
			# if not password, try to do it in the traditional way
			if os.path.exists(destModFile):
				os.remove(destModFile)
			shutil.copy(originModFile, userModulesPath)

		print ("File toolCageInit.mod created in user " + username + ": " + destModFile)
		return (os.path.exists(destModFile))
	else:
		return False

def unistallModToUser(username, password=None):
	currentUser = getpass.getuser()
	currentUserFolder = "/usr/people/" + currentUser
	currentMachine = socket.gethostname().replace(".mpc.local", "")

	userModulesPath = "/usr/people/" + username + "/maya/2015-x64/modules/"
	destModFile = userModulesPath + "toolCageInit.mod"

	if os.path.exists(destModFile):
		if password is not None:
			# if password, try to use mpcsu to remove the file

			deployRmMpcsuFile = os.path.dirname(__file__) + "/deploy-installModToUser-mpcsu-rm.exp"
			deployRmMpcsuFileForUser = currentUserFolder + "/deploy-installModToUser-mpcsu-rm.exp"
			
			# duplicate the file and modify the content for the current execution
			replacements = {"_destUser_":username, "_currentUser_":currentUser, "_currentMachine_":currentMachine, "_password_":password}

			data = open(deployRmMpcsuFile).read()
			outfile = open(deployRmMpcsuFileForUser, 'w')

			for i in replacements.keys():
				data = data.replace(i, replacements[i])
				
			outfile.write(data)
			outfile.close()

			if os.path.exists(deployRmMpcsuFileForUser):
				p2 = subprocess.Popen(["expect", deployRmMpcsuFileForUser], stdout=subprocess.PIPE)
				output, err = p2.communicate()
				
				os.remove(deployRmMpcsuFileForUser)
		else:
			# if not password, try to do it in the traditional way
			os.remove(destModFile)

		print ("File toolCageInit.mod removed in user " + username + ": " + destModFile)
		return (not os.path.exists(destModFile))
	else:
		return True


#######################################
# execution

if __name__ == "__main__":
	# print (installModToUser("benoit-d", password="EralDream01"))
	# print (unistallModToUser("benoit-d", password="EralDream01"))
	# deployCurrentToolCageDev()
	pass