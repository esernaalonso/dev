#######################################
# imports

import sys, os, inspect
import ctypes

from PySide import QtCore, QtGui
from PySide.phonon import Phonon
from PySide import phonon

import esa.common.python.lib.utils as utils
import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.media.video as video
import esa.common.python.lib.image.image as image
import esa.common.python.lib.theme.theme as theme
import esa.common.python.tool.inside_anim.campus.credential.credential as credential

reload(utils)
reload(ui)
reload(video)
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

        # Applies the theme for the widget
        # theme.apply_style(self, "inside_anim_dark.qss")

        # Icon for the window
        image_app_icon = image.get_image_file("app_icon.png", self.get_current_folder())
        self.setWindowIcon(image.create_pixmap(image_app_icon))

        # Allows maximize and minimize
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)

        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWiget = InsideAnimCampusMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)

        self.show()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def closeEvent(self, event):
        self.opened = False


class InsideAnimCampusMainWidget(QtGui.QWidget):
    def __init__(self):
        super(InsideAnimCampusMainWidget, self).__init__()
        self.credentials = credential.Credentials()
        # self.initLoginUI()
        self.initUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initLoginUI(self):
        # Load UI file.
        main_ui_file = ui.get_ui_file("login.ui", self.get_current_folder())
        self.ui = ui.loadUiWidget(main_ui_file, parent=self)

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
        self.ui = ui.loadUiWidget(main_ui_file, parent=self)

        # Layout
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        test_video_link = QtCore.QUrl("http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt02_animal_anatomy_vs_human_anatomy.flv")
        self.wg_test_video = ui.get_child(self.ui, "wg_test_video")
        self.video_player = video.video_player_widget()
        self.wg_test_video.layout().addWidget(self.video_player)
        self.video_player.set_url(test_video_link, framerate=25)
        theme.apply_style(self.wg_test_video, "video_player.qss")


def InsideAnimCampusRun():
    # Creates the application
    app = QtGui.QApplication(sys.argv)

    # Applies the theme for the application
    theme.apply_style(app, "inside_anim_dark.qss")

    # If windows, indicates the process is a separate one to allow the taskbar to use the window icon.
    if os.name == "nt":
        myappid = 'custom.process.inside_anim.campus' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Creates the aplication execution and UI
    execution = InsideAnimCampus()

    # Enters the application loop
    sys.exit(app.exec_())


def InsideAnimCampusClose():
    utils.closeTool('InsideAnimCampus')

#######################################
# execution
if __name__ == "__main__":
    InsideAnimCampusRun()
