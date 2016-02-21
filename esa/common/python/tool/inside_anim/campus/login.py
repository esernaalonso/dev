#######################################
# imports

# import maya.cmds as cmds
# import maya.OpenMayaUI as apiUI
import sys, os, inspect

from PySide import QtCore, QtGui

import esa.common.python.lib.utils as utils
import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.theme.theme as theme

reload(ui)
reload(theme)

#######################################
# attributes

permission = "developer"

#######################################
# functionality


class InsideAnimCampus(QtGui.QDialog):
    def __init__(self,  parent=None):
        super(InsideAnimCampus, self).__init__(parent)

        self.setObjectName('InsideAnimCampus')
        self.opened = True

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("Inside Animation Campus")

        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWiget = InsideAnimCampusMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)

        self.show()

    def closeEvent(self, event):
        self.opened = False


class InsideAnimCampusMainWidget(QtGui.QWidget):
    def __init__(self):
        super(InsideAnimCampusMainWidget, self).__init__()
        self.initUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def initUI(self):
        # Load UI file
        current_file = self.get_current_file()
        current_folder = os.path.dirname(current_file)
        main_ui_file = ui.get_ui_file("main.ui", current_folder)
        self.ui = ui.loadUiWidgetFromPyFile(main_ui_file, parent=self)

        # Layout
        # self.setMinimumSize(200, 100)

        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Store ui elements for use later in signals or functions

        # self.sld_cartoon_level = ui.get_child(self.ui, "sld_cartoon_level")
        # self.rb_drama = ui.get_child(self.ui, "rb_drama")
        # self.rb_comedy = ui.get_child(self.ui, "rb_comedy")
        # self.rb_mistery = ui.get_child(self.ui, "rb_mistery")
        # self.pb_apply = ui.get_child(self.ui, "pb_apply")
        # self.pb_unapply = ui.get_child(self.ui, "pb_unapply")
        # self.pb_para_final = ui.get_child(self.ui, "pb_para_final")

        # Connect signals

        # self.pb_para_final.clicked.connect(self.make_film)
        # self.pb_apply.clicked.connect(self.make_film)
        # self.pb_unapply.clicked.connect(self.make_film)


def InsideAnimCampusRun():
    app = QtGui.QApplication(sys.argv)
    theme.apply_style(app, "inside_anim_dark.qss")
    test = InsideAnimCampus()
    sys.exit(app.exec_())


def InsideAnimCampusClose():
    utils.closeTool('InsideAnimCampus')

#######################################
# execution
if __name__ == "__main__":
    InsideAnimCampusRun()
