#######################################
# imports

# import maya.cmds as cmds
# import maya.OpenMayaUI as apiUI
import sys, os, inspect

from PySide import QtCore, QtGui

import esa.common.python.lib.utils as utils
import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.image.image as image
import esa.common.python.lib.theme.theme as theme
import esa.common.python.tool.inside_anim.campus.credential.credential as credential

reload(utils)
reload(ui)
reload(theme)
reload(credential)

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
        self.credentials = credential.Credentials()
        self.initLoginUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initLoginUI(self):
        # Load UI file.
        current_file = self.get_current_file()
        current_folder = os.path.dirname(current_file)
        main_ui_file = ui.get_ui_file("login.ui", current_folder)
        self.ui = ui.loadUiWidgetFromPyFile(main_ui_file, parent=self)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Store ui elements for use later in signals or functions.
        self.lb_image_logo = ui.get_child(self.ui, "lb_image_logo")
        self.lb_image_title = ui.get_child(self.ui, "lb_image_title")
        self.le_user = ui.get_child(self.ui, "le_user")
        self.le_pass = ui.get_child(self.ui, "le_pass")
        self.lb_info = ui.get_child(self.ui, "lb_info")
        self.pb_login = ui.get_child(self.ui, "pb_login")

        # Set the ui images.
        image_logo_file = image.get_image_file("login_logo.png", self.get_current_folder())
        image_title_file = image.get_image_file("login_title.png", self.get_current_folder())
        self.lb_image_logo.setPixmap(image.create_pixmap(image_logo_file))
        self.lb_image_title.setPixmap(image.create_pixmap(image_title_file))

        # Connect signals
        self.pb_login.clicked.connect(self.check_login)

    def check_login(self):
        self.credentials.validate(self.le_user.text(), self.le_pass.text())
        self.lb_info.setText(self.credentials.get_connection_message())

        if self.credentials.is_validated():
            while self.layout().count():
                self.layout().takeAt(0).widget().setParent(None)
            self.initUI()

    def initUI(self):
        # Load UI file
        current_file = self.get_current_file()
        current_folder = os.path.dirname(current_file)
        main_ui_file = ui.get_ui_file("main.ui", current_folder)
        self.ui = ui.loadUiWidgetFromPyFile(main_ui_file, parent=self)

        # Layout
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)


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
