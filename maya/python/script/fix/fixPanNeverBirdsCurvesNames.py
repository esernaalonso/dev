#############################################################################################
# This functions are for fixing pan neverbirds curves names.
#############################################################################################

#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import sys

#######################################
# attributes

permission = "artist"

#######################################
# functionality

class fixPanNeverBirdsCurvesNames():
	def __init__(self):
		pass

	# return all nodes that need to be fixed
	def getNodesToFix(self):
		nodesToFix = cmds.ls("*:*:hubAnimCurvesNeverBirdASet")
		nodesToFix += cmds.ls("*:*:hubAnimPoseNeverBirdASet")
		nodesToFix += cmds.ls("*:*:hubAnimCurvesNeverbirdASet")
		nodesToFix += cmds.ls("*:*:hubAnimPoseNeverbirdASet")
		return nodesToFix

	# fixes all attributes that need to be fixed in nodeToFix node.
	# returns True if success and False if not.
	def fixNode(self, nodeToFix, invert=False):
		print ("\n" + nodeToFix)

		# gets all attributes that need to be fixed
		attrs = cmds.listAttr(nodeToFix, st=["hubElement"])
		for attr in attrs:
			print ("Found Attribute -> '" + attr + "'")
			
			# check if the attribute is empty and if yes, fixs it
			val = cmds.getAttr(nodeToFix + "." + attr)

			condition = (not val or val != "neverBirdA")
			if invert: condition = (val == "neverBirdA")

			if condition:
				msg = ("Attribute '" + attr + "' is empty or incorrect.")
				if invert: msg = ("Attribute '" + attr + "' is OK.")
				print msg

				# if the attribute is locked, unlocks it first
				isLocked = cmds.getAttr((nodeToFix + "." + attr), lock=True)
				if isLocked:
					print ("Attribute '" + attr + "' is locked. Unlocking it.")
					isReferenced = cmds.referenceQuery((nodeToFix + "." + attr), isNodeReferenced=True)
					if isReferenced:
						try:
							cmds.setAttr((nodeToFix + "." + attr), lock=False)
						except:
							print ("Attribute '" + attr + "' could not be unlocked, it is referenced.")
					else:
						cmds.setAttr((nodeToFix + "." + attr), lock=False)

				# if the attribute is now unlocked, fixes the value
				isLocked = cmds.getAttr((nodeToFix + "." + attr), lock=True)
				if not isLocked:
					msg = ("Attribute '" + attr + "'. Setting value to 'neverBirdA'")
					if invert: msg = ("Attribute '" + attr + "'. Setting value to 'empty string'.")
					print msg

					newVal = "neverBirdA"
					if invert: newVal = ""
					
					print (nodeToFix + "." + attr)
					print (cmds.getAttr((nodeToFix + "." + attr), settable=True))

					cmds.setAttr((nodeToFix + "." + attr), newVal, type="string")
					
					isReferenced = cmds.referenceQuery((nodeToFix + "." + attr), isNodeReferenced=True)
					if not isReferenced:
						print ("Attribute '" + attr + "'. Locking again")
						cmds.setAttr((nodeToFix + "." + attr), lock=True)
					else:
						print ("Attribute '" + attr + "'. Is referenced, unable to locl again.")
				else:
					print ("Attribute '" + attr + "' could not be unlocked.")

			else:
				msg = ("Attribute '" + attr + "' is OK -> '" + val + "'")
				if invert: msg = ("Attribute '" + attr + "' is not OK.")
				print msg

	# Fixes all nodes that have bad anim curves names
	def fix(self, invert=False):
		print "\n--------------------------------------------------------------------"
		print "Fixing bad anim curves names for (PAN NEVERBIRDS)..."

		nodesToFix = self.getNodesToFix()
		for n in nodesToFix:
			self.fixNode(nodeToFix=n, invert=invert)

		print "\n...all curves fixed for (PAN NEVERBIRDS)"
		print "--------------------------------------------------------------------"

def fixPanNeverBirdsCurvesNamesRun():
	fixer = fixPanNeverBirdsCurvesNames()
	fixer.fix()

#######################################
# execution
if __name__ == "__main__": fixPanNeverBirdsCurvesNamesRun()