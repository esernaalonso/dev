#######################################
# imports

import maya.cmds as cmds
import maya.OpenMayaUI as apiUI

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui
import esa.maya.python.lib.deploy as deploy

reload(utils)
reload(ui)
reload(deploy)

#######################################
# attributes

permission = "developer"

#######################################
# functionality

class InstallToolCageToUser(QtGui.QDialog):
	def __init__(self,  parent=utils.getMayaWindow()):
		super(InstallToolCageToUser, self).__init__(parent)
		
		self.setObjectName('installToolCageToUser')
		self.opened = True
		
		self.initUI()

	def initUI(self):
		# Title
		self.setWindowTitle("Tool Cage Install to User")

		# layout
		self.setLayout(QtGui.QVBoxLayout())
				
		# add main widget
		self.mainWiget = InstallToolCageToUserMainWidget()
		self.layout().addWidget(self.mainWiget)
		self.layout().setSpacing(0)
		
		self.show()

	def closeEvent(self, event):
		self.opened = False

class InstallToolCageToUserMainWidget(QtGui.QWidget):
	def __init__(self, parent=None):
		super(InstallToolCageToUserMainWidget, self).__init__(parent)
		self.initUI()

	def initUI(self):
		# self.setMinimumSize(200, 100)

		self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

		# layout
		self.setLayout(QtGui.QVBoxLayout())
		self.layout().addWidget(self.ui)
		self.layout().setSpacing(0)
		self.layout().setContentsMargins(2, 2, 2, 2)

		# fill UI info

		# add signals to the ui elements
		self.ui.pb_install.clicked.connect(self.installToolCage)
		self.ui.pb_uninstall.clicked.connect(self.uninstallToolCage)

	def installToolCage(self):
		# only if the user text field is not empty
		if (self.ui.le_userNames.text() != ""):
			# this is a delicate operation and needs confirmation
			answer = cmds.confirmDialog(t="Alert", message="The install operation has no undo, do you want to continue?", button=["Cancel", "Yes"], icon="warning")

			# if we choose to continue
			if answer == "Yes":
				# gets the password
				currPassword = self.ui.le_password.text()
				if currPassword == "":
					currPassword = None

				# lists for the success or error install users
				successUsers = []
				errorUsers = []

				# loops the users installing
				userNames = self.ui.le_userNames.text().split(" ")

				cmds.waitCursor(state=True)
				for usr in userNames:
					success = (deploy.installModToUser(usr, password=currPassword))
					
					if success: successUsers.append(usr)
					else: errorUsers.append(usr)
				cmds.waitCursor(state=False)

				message = ""

				if len(successUsers) > 0:
					message += "Installed successfully to:"
					for usr in successUsers:
						message += "\n" + usr
					if len(errorUsers) > 0: message += "\n\n"

				if len(errorUsers) > 0:
					message += "Error installing to:"
					for usr in errorUsers:
						message += "\n" + usr

				cmds.confirmDialog(t="Finished", message=message, button=["OK"], icon="information")

				self.ui.le_userNames.setText("")
				self.ui.le_password.setText("")

	def uninstallToolCage(self):
		# only if the user text field is not empty
		if (self.ui.le_userNames.text() != ""):
			# this is a delicate operation and needs confirmation
			answer = cmds.confirmDialog(t="Alert", message="The uninstall operation has no undo, do you want to continue?", button=["Cancel", "Yes"], icon="warning")

			# if we choose to continue
			if answer == "Yes":
				# gets the password
				currPassword = self.ui.le_password.text()
				if currPassword == "":
					currPassword = None

				# lists for the success or error install users
				successUsers = []
				errorUsers = []

				# loops the users installing
				userNames = self.ui.le_userNames.text().split(" ")

				cmds.waitCursor(state=True)
				for usr in userNames:
					success = (deploy.unistallModToUser(usr, password=currPassword))
					
					if success: successUsers.append(usr)
					else: errorUsers.append(usr)
				cmds.waitCursor(state=False)

				message = ""

				if len(successUsers) > 0:
					message += "Uninstalled successfully to:"
					for usr in successUsers:
						message += "\n" + usr
					if len(errorUsers) > 0: message += "\n\n"

				if len(errorUsers) > 0:
					message += "Error uninstalling to:"
					for usr in errorUsers:
						message += "\n" + usr

				cmds.confirmDialog(t="Finished", message=message, button=["OK"], icon="information")

				self.ui.le_userNames.setText("")
				self.ui.le_password.setText("")

def installToolCageToUserRun():
	utils.closeTool('installToolCageToUser')
	dTool = InstallToolCageToUser()

def installToolCageToUserClose():
	utils.closeTool('installToolCageToUser')
	
#######################################
# execution
if __name__ == "__main__": installToolCageToUserRun()
