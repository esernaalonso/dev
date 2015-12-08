#######################################
# imports

import maya.cmds as cmds

from PySide import QtCore, QtGui

import esa.maya.python.lib.utils as utils

reload(utils)

#######################################
# attributes

permission = "artist"

#######################################
# functionality


class NodeEditor(QtGui.QDialog):
    def __init__(self,  parent=utils.getMayaWindow()):
        super(NodeEditor, self).__init__(parent)

        self.setObjectName('nodeEditor')
        self.opened = True

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("Node Editor")

        # layout
        self.setLayout(QtGui.QVBoxLayout())
        self.resize(500, 300)

        # add main widget
        self.mainWiget = NodeEditorMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.show()

    def closeEvent(self, event):
        self.opened = False


class NodeEditorMainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(NodeEditorMainWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(200, 100)
        # self.resize(600,400)

        # layout
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        self.nodeEditor = cmds.scriptedPanel(type="nodeEditorPanel", label="Node Editor")
        pySideNodeEditor = utils.mayaWindowToPySideWidget(self.nodeEditor)
        self.layout().addWidget(pySideNodeEditor)


def nodeEditorRun():
    utils.closeTool('nodeEditor')
    NodeEditor()


def nodeEditorClose():
    utils.closeTool('nodeEditor')

#######################################
# execution
if __name__ == "__main__":
	nodeEditorRun()
