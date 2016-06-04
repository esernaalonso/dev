#######################################
# imports

import glob
import os
import subprocess

import esa.maya.python.lib.string as string

reload(string)

#######################################
# functionality

def getImageFilesFromPath(imagesPath, imageType=".jpg"):
	"""
		Returns all image files in the given path that uses the given extension.
		imagesPath: It needs a path to get files from.
		imageType: It needs a file extension.
	"""
	# imagesPath = os.path.dirname(imagesPath + "/")

	imagePattern = (imagesPath + "/*" + imageType)
	return glob.glob(imagePattern)

def createGIFanimFromPath(imagesPath, scale=1.0, colors=256, imageType=".jpg"):
	"""
		Creates a new gif animation file from the image files in the given path.
		imagesPath: It needs a path to get files from.
		scale: The final size of the gif can be modified scaling the original.
		colors: The number of gif colors can be reduced to reduce file size.
		imageType: It needs a file extension.
	"""
	# imagesPath = os.path.dirname(imagesPath + "/")

	imageFiles = getImageFilesFromPath(imagesPath, imageType=imageType)

	if len(imageFiles) > 0:
		imagesToGIFpattern = string.getLongestCommonSubstr(imageFiles) + "*" + imageType
		print imagesToGIFpattern

		animGIFpathTemp = imagesPath + "/" + os.path.basename(os.path.normpath(imagesPath)) + "Temp.gif"
		print animGIFpathTemp

		animGIFpath = imagesPath + "/" + os.path.basename(os.path.normpath(imagesPath)) + ".gif"
		print animGIFpath

		# removes the gif in case ther is an old version
		if os.path.exists(animGIFpath):
			os.remove(animGIFpath)

		# creates the gif anim
		p = subprocess.Popen(["convert", "-layers", "optimize", "-delay", "0", imagesToGIFpattern, animGIFpathTemp], stdout=subprocess.PIPE)
		output, err = p.communicate()
		print "Running GIF creation command:\n", output

		# optimizes the gif
		p2 = subprocess.Popen(["gifsicle", "--scale", str(scale), "-O3", "--colors", str(colors), animGIFpathTemp, "-o", animGIFpath], stdout=subprocess.PIPE)
		output, err = p2.communicate()
		print "Running GIF optimization command:\n", output

		os.remove(animGIFpathTemp)
		return animGIFpath
	else:
		return None	

def createGIFanimFromPlayblast(playBlastPath, scale=1.0, colors=256, openAtEndMode="firefox"):
	"""
		Creates a new gif animation file from the image files in the given playblast path.
		playBlastPath: It needs a path to get files from.
		scale: The final size of the gif can be modified scaling the original.
		colors: The number of gif colors can be reduced to reduce file size.
		openAtEndMode: Indicates what to do at end.
			firefox: Open it in firefox new window.
			folder: Open the containing folder in a new browser.
			None: Does nothing.
	"""
	# playBlastPath = os.path.dirname(playBlastPath + "/")

	if os.path.exists(playBlastPath):
		print "Create GIF from playblast -> " + playBlastPath
		playblastGIFfilePath = createGIFanimFromPath(playBlastPath, scale=scale, colors=colors)

		if openAtEndMode == "firefox":
			p = subprocess.Popen(["firefox", playblastGIFfilePath], stdout=subprocess.PIPE)
			output, err = p.communicate()
			print "Opening GIF in firefox:\n", output
	else:
		print "Unable to create GIF from playblast, path doesn't exist -> " + playBlastPath

#######################################
# testing

def test001():
	print "test playblast to gif - 001"
	playblastPath = "/jobs/vst/rnd/rnd_sequence/maya/playblasts/rnd_sequence_testImportCaches_005_1"
	createGIFanimFromPlayblast(playblastPath, scale=0.75, colors=128)

#######################################
# execution

if __name__ == "__main__":
	# test001()
	pass
	