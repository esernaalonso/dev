#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys
import time

from mpc import jobtools as jobTls

#######################################
# functionality

def getJob():
	""" Return the job from the environment.

		Returns:
			(str or None): Job, or None if no job is found.
	"""
	return jobTls.jobName()

def getScene():
	""" Returns the scene from the environment.

		Returns:
			(str or None): Scene, or None if no scene is found.
	"""
	return jobTls.sceneName()

def getShot():
	""" Returns the shot from the environment.

		Returns:
			(str or None): Shot, or None if no shot is found.
	"""
	return jobTls.shotName()

def getPlayblastPath():
	jobName = jobTls.jobName()
	sceneName = jobTls.sceneName()
	shotName = jobTls.shotName()
	
	if jobName and sceneName and shotName:
		return ("/jobs/" + jobName + "/" + sceneName + "/" + shotName + "/maya/playblasts/")
	else:
		return None

#######################################
# execution
if __name__ == "__main__":
	pass