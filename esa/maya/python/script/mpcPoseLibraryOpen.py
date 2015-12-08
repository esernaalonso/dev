#######################################
# imports

import os

from mpc import jobtools as _jobTools

#######################################
# attributes

permission = "artist"

#######################################
# functionality

def runPoseLibrary():
	""" launches studio library
	"""
	superusers = []
	
	# try and read the config file
	configFilePath = os.path.join("/jobs", _jobTools.jobName(), "config", "animationTools", "poseLibrary", "superusers.conf")
	if os.path.exists(configFilePath):
		with open(configFilePath, "r") as f:
			for line in f.readlines():
				superusers.append(line.rstrip())
	
	# launch studio library
	import studioLibrary

	if superusers:
		studioLibrary.main(root="/jobs/ttu/library/studioLibrary", superusers=superusers, lockFolder="approved")
	else:
		studioLibrary.main(root="/jobs/ttu/library/studioLibrary")

def mpcPoseLibraryOpenRun():
	runPoseLibrary()

#######################################
# execution

if __name__ == "__main__": mpcPoseLibraryOpenRun()