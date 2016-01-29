#######################################
# imports

# import maya.cmds as cmds
# import maya.OpenMayaUI as apiUI
import sys
import os

from PySide import QtCore, QtGui, QtXml

import esa.common.python.lib.utils as utils
import esa.common.python.lib.ui.ui as ui
#
# reload(utils)
reload(ui)

#######################################
# attributes

permission = "developer"

#######################################
# functionality


# def get_current_file():
#     if getattr(sys, 'frozen', False):
#         # frozen
#         print os.path.dirname(sys.executable)
#         return os.path.dirname(sys.executable)
#     else:
#         # unfrozen
#         print os.path.realpath(__file__)
#         return os.path.realpath(__file__)


class TemplateToolStdUI(QtGui.QDialog):
    def __init__(self,  parent=None):
        super(TemplateToolStdUI, self).__init__(parent)

        self.setObjectName('templateToolStdUI')
        self.opened = True

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("Osom Template Tool")

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
    def __init__(self):
        super(TemplateToolStdUIMainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # Load UI file

        self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

        # Layout
        # self.setMinimumSize(200, 100)

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Store ui elements for use later in signals or functions

        self.sld_cartoon_level = ui.get_child(self.ui, "sld_cartoon_level")
        self.rb_drama = ui.get_child(self.ui, "rb_drama")
        self.rb_comedy = ui.get_child(self.ui, "rb_comedy")
        self.rb_mistery = ui.get_child(self.ui, "rb_mistery")
        self.pb_apply = ui.get_child(self.ui, "pb_apply")
        self.pb_unapply = ui.get_child(self.ui, "pb_unapply")
        self.pb_para_final = ui.get_child(self.ui, "pb_para_final")

        # Connect signals

        self.pb_para_final.clicked.connect(self.make_film)
        self.pb_apply.clicked.connect(self.make_film)
        self.pb_unapply.clicked.connect(self.make_film)

    def make_film(self):
        print "======================================================================================"
        print "We are making a cartoon-realist film level %s." % str(self.sld_cartoon_level.value())
        print "More or less, is a %s film." % ("drama" if self.rb_drama.isChecked() else ("comedy" if self.rb_comedy.isChecked() else "mistery"))
        print "======================================================================================"


def templateToolStdUIRun():
    app = QtGui.QApplication(sys.argv)
    test = TemplateToolStdUI()
    sys.exit(app.exec_())


def templateToolStdUIClose():
    utils.closeTool('templateToolStdUI')

#######################################
# execution
if __name__ == "__main__":
    templateToolStdUIRun()
