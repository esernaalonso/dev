#######################################
# imports

import os
import json
import getpass

#######################################
# functionality

def getUserPermissionLevel():
	permissionLevel = "artist"

	# file where the permissions are stored
	permissionsFile = (__file__.replace(".pyc", ".conf")).replace(".py", ".conf")
	
	# if the permission file exists try to find the user in one of the permission levels
	if os.path.exists(permissionsFile):
		f = open(permissionsFile)
		jsonFileData = f.read()
		f.close()
		jsonData = json.loads(jsonFileData)

		# get the current user in the system
		currentUser = getpass.getuser()

		# loops the levels and search the user
		for pLevel in jsonData.keys():
			pLevelUsers = jsonData[pLevel]
			for usr in pLevelUsers:
				if currentUser == usr["name"]:
					permissionLevel = pLevel

	return permissionLevel

#######################################
# execution

if __name__ == "__main__":
	# print "lib execution"
	# print (getUserPermissionLevel())
	pass