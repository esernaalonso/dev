#######################################
# imports

from PySide import QtCore, QtGui, QtUiTools
from shiboken import wrapInstance

import maya.OpenMayaUI as apiUI
import shiboken

#######################################
# definitions


def getMayaWindow():
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtGui.QMainWindow)


def closeTool(toolName, dock=False):
    mayaWindow = getMayaWindow()
    tool = mayaWindow.findChild(QtGui.QDialog, toolName)
    if tool:
        if (not dock):
            shiboken.delete(tool)
        else:
            tool.close()

        tool = None


def loadUiWidget(uifilename, parent=None):
    """Loads an ui file from a given file.

    Args:
        uifilename (str): Path file of the .ui file to load.
        parent (QWidget, optional): Optional parent for the given ui.

    Returns:
        QWidget: Returns the loaded widget.
    """
    loader = QtUiTools.QUiLoader()

    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)

    oUi = loader.load(uifile, parent)

    uifile.close()

    return oUi


def loadUiWidgetFromPyFile(uifilename, parent=None):
    """Loads the equivalent ui widget from a py file.

    Args:
        uifilename (str): Path file of the .py file whose .ui load.
        parent (QWidget, optional): Optional parent for the given ui.

    Returns:
        QWidget: Returns the loaded widget.
    """
    sUIfile = uifilename.replace(".pyc", ".ui")
    sUIfile = sUIfile.replace(".py", ".ui")

    return loadUiWidget(sUIfile, parent=parent)


def get_child(root_element, name):
    """Summary

    Args:
        root_element (QtCore.QObject): UI object root to search recursive the child that has the given name.
        name (str): The name of the ui element that is searched.

    Returns:
        QtCore.QObject: UI object that uses the given name.
    """
    if root_element:
        children = root_element.findChildren(QtCore.QObject, name)
        if children:
            return children[0]

    return None


def templateToolStdUIRun():
    closeTool('templateToolStdUI')
    TemplateToolStdUI()


def templateToolStdUIClose():
    closeTool('templateToolStdUI')


#######################################
# classes

class TemplateToolStdUI(QtGui.QDialog):
    def __init__(self,  parent=getMayaWindow()):
        super(TemplateToolStdUI, self).__init__(parent)

        self.setObjectName('templateToolStdUI')
        self.opened = True

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("Osom Hater Tool")

        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWiget = TemplateToolStdUIMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)

        self.show()

    def closeEvent(self, event):
        self.opened = False


class TemplateToolStdUIMainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TemplateToolStdUIMainWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # Load UI file

        self.ui = loadUiWidgetFromPyFile(__file__, parent=self)

        # Layout

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Store ui elements for use later in signals or functions

        self.sld_cartoon_level = get_child(self.ui, "sld_cartoon_level")
        self.rb_drama = get_child(self.ui, "rb_drama")
        self.rb_comedy = get_child(self.ui, "rb_comedy")
        self.rb_mistery = get_child(self.ui, "rb_mistery")
        self.pb_apply = get_child(self.ui, "pb_apply")
        self.pb_unapply = get_child(self.ui, "pb_unapply")
        self.pb_para_final = get_child(self.ui, "pb_para_final")

        # Connect signals

        self.pb_para_final.clicked.connect(self.make_film)
        self.pb_apply.clicked.connect(self.make_film)
        self.pb_unapply.clicked.connect(self.make_film)

    def make_film(self):
        print "======================================================================================"
        print "We are making a cartoon-realist film level %s." % str(self.sld_cartoon_level.value())
        print "More or less, is a %s film." % ("drama" if self.rb_drama.isChecked() else ("comedy" if self.rb_comedy.isChecked() else "mistery"))
        print "======================================================================================"


#######################################
# execution
if __name__ == "__main__":
    templateToolStdUIRun()
