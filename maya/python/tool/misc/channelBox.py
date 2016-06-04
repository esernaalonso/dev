#######################################
# imports

import maya.cmds as cmds
import pymel.core as pm

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils

reload(utils)

#######################################
# attributes

permission = "artist"

#######################################
# functionality


class ChannelBox(QtGui.QDialog):
    def __init__(self,  parent=utils.getMayaWindow()):
        super(ChannelBox, self).__init__(parent)

        self.setObjectName('channelBox')
        self.opened = True

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("Channel Box")

        # layout
        self.setLayout(QtGui.QVBoxLayout())
        self.resize(500, 300)

        # add main widget
        self.mainWiget = ChannelBoxMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.show()

    def closeEvent(self, event):
        self.opened = False


class ChannelBoxMainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ChannelBoxMainWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(200, 100)

        # layout
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.channelBox = pm.channelBox('channelBox')
        pySideChannelBox = utils.mayaWindowToPySideWidget(self.channelBox)
        self.layout().addWidget(pySideChannelBox)


def channelBoxRun():
    utils.closeTool('channelBox')
    ChannelBox()


def channelBoxClose():
    utils.closeTool('channelBox')

#######################################
# execution
if __name__ == "__main__":
    channelBoxRun()
