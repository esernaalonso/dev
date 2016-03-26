#######################################
# imports

import sys
import os
import inspect
import re
import random
import ctypes

from PySide import QtCore, QtGui

import esa.common.python.lib.utils as utils
import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.io.io as io
import esa.common.python.lib.media.video as video
import esa.common.python.lib.media.video_player as video_player
import esa.common.python.lib.image.image as image
import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.logger.logger as logger
import esa.common.python.lib.osys.power_management as power_management

reload(utils)
reload(ui)
reload(video)
reload(image)
reload(theme)
reload(logger)
reload(power_management)

#######################################
# attributes

permission = "artist"

#######################################
# functionality


class ESAPlayer(QtGui.QDialog):
    def __init__(self,  parent=None):
        super(ESAPlayer, self).__init__(parent)

        self.setObjectName('ESAPlayer')
        self.opened = True

        power_management.prevent_standby()

        self.initUI()

    def initUI(self):
        # Title
        self.setWindowTitle("ESA Player")

        # Applies the theme for the widget
        # theme.apply_style(self, "esa_dark.qss")

        # Icon for the window
        image_app_icon = image.get_image_file("play_yellow.png", self.get_current_folder())
        self.setWindowIcon(image.create_pixmap(image_app_icon))

        # Allows maximize and minimize
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMinMaxButtonsHint)

        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWiget = ESAPlayerMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(4, 4, 4, 4)

        # resizesthe interface to get the initial default.
        self.resize(1024, 418)

        self.show()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def closeEvent(self, event):
        power_management.allow_standby()
        self.opened = False


class ESAPlayerMainWidget(QtGui.QWidget):
    def __init__(self):
        super(ESAPlayerMainWidget, self).__init__()

        # To store the current forlder to work with.
        self.current_folder = None

        # Flag to avoid loops in UI fill and refresh
        self.updating_ui = False

        # Allowed extensions
        self.allowed_extensions = [".avi", ".flv", ".mkv", ".mp4", ".mov"]

        self.initUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initUI(self):
        # Load UI file
        current_file = self.get_current_file()
        current_folder = os.path.dirname(current_file)
        main_ui_file = ui.get_ui_file("esa_player.ui", current_folder)
        self.ui = ui.loadUiWidget(main_ui_file, parent=self)

        # Layout
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # Store ui elements for use later in signals or functions.
        self.le_folder = ui.get_child(self.ui, "le_folder")
        self.pb_folder = ui.get_child(self.ui, "pb_folder")
        self.cbx_categories = ui.get_child(self.ui, "cbx_categories")
        self.le_filter = ui.get_child(self.ui, "le_filter")
        self.pb_filter = ui.get_child(self.ui, "pb_filter")
        self.pb_clear = ui.get_child(self.ui, "pb_clear")
        self.lw_video = ui.get_child(self.ui, "lw_video")
        self.lb_playing_name = ui.get_child(self.ui, "lb_playing_name")

        self.wg_video_player = ui.get_child(self.ui, "wg_video_player")
        self.video_player = video_player.video_player_widget()
        self.wg_video_player.layout().addWidget(self.video_player)
        theme.apply_style(self.wg_video_player, "video_player.qss")
        self.video_player.set_step_options(mode="percent", size=0.01, pause_on_step=False)
        self.set_video_player_state(False)

        self.pb_track_prev = ui.get_child(self.ui, "pb_track_prev")
        self.pb_track_next = ui.get_child(self.ui, "pb_track_next")
        self.pb_loop = ui.get_child(self.ui, "pb_loop")
        self.pb_random = ui.get_child(self.ui, "pb_random")

        # Set the ui images.
        self.pb_folder.setIcon(image.create_pixmap(image.get_image_file("folder.png", self.get_current_folder())))
        self.pb_filter.setIcon(image.create_pixmap(image.get_image_file("search.png", self.get_current_folder())))
        self.pb_clear.setIcon(image.create_pixmap(image.get_image_file("eraser.png", self.get_current_folder())))

        self.pb_loop.setIcon(image.create_pixmap(image.get_image_file("loop.png", self.get_current_folder())))
        self.pb_random.setIcon(image.create_pixmap(image.get_image_file("random.png", self.get_current_folder())))

        # Signals
        self.pb_folder.released.connect(self.choose_folder)
        self.cbx_categories.currentIndexChanged.connect(self.fill_video_list)
        self.le_filter.returnPressed.connect(self.fill_video_list)
        self.pb_filter.clicked.connect(self.fill_video_list)
        self.pb_clear.clicked.connect(self.clear_filters)
        # self.lw_video.itemDoubleClicked.connect(self.play_video)
        self.lw_video.itemSelectionChanged.connect(self.play_video)
        # self.lw_video.itemEntered.connect(self.play_video)
        # self.pb_loop.toggled.connect(self.update_icons)
        # self.pb_random.toggled.connect(self.update_icons)
        self.pb_track_prev.clicked.connect(self.play_prev)
        self.pb_track_next.clicked.connect(self.play_next)

    # def update_icons(self):
    #     """ Function to update some icons depending on the state of the ui controls.
    #     """
    #     if self.pb_loop.isChecked():
    #         self.pb_loop.setIcon(image.create_pixmap(image.get_image_file("loop_checked.png", self.get_current_folder())))
    #     else:
    #         self.pb_loop.setIcon(image.create_pixmap(image.get_image_file("loop.png", self.get_current_folder())))
    #
    #     if self.pb_random.isChecked():
    #         self.pb_random.setIcon(image.create_pixmap(image.get_image_file("random_checked.png", self.get_current_folder())))
    #     else:
    #         self.pb_random.setIcon(image.create_pixmap(image.get_image_file("random.png", self.get_current_folder())))

    def video_player_state_changed(self):
        """ Operations to do when the player state changes.
        """
        if self.video_player.is_ready():
            pass
            # TODO: In case of we want to perform operations in the future when state changes.

    def set_video_player_state(self, state):
        """ Hides or shows the video player controls bar and the enabled state for the player widget

        state (bool): New state.
        """
        self.wg_video_player.setEnabled(state)
        self.video_player.wg_controls_bar.setVisible(state)

    def change_track(self, direction="next"):
        """ Jumps to the next / prev item to play or random.

            Args:
                direction (str, optional): Indicates if go to next or prev
        """

        current_index = self.lw_video.currentRow()
        new_index = current_index

        if direction == "next":
            new_index = (current_index + 1) if (current_index + 1) < self.lw_video.count() else 0
        if direction == "prev":
            new_index = (current_index - 1) if (current_index - 1) >= 0 else (self.lw_video.count() - 1)

        if self.pb_random.isChecked():
            new_index = random.randint(0, self.lw_video.count() - 1)

        if new_index != current_index:
            self.lw_video.setCurrentRow(new_index)

    def play_prev(self):
        """ Jumps to the prev item to play
        """
        self.change_track(direction="prev")

    def play_next(self):
        """ Jumps to the next item to play
        """
        self.change_track(direction="next")

    def loop(self):
        if self.pb_loop.isChecked():
            self.play_next()

    def play_video(self):
        """ Plays the selected video in the player.
        """
        if self.video_player.is_ready():
            try:
                self.video_player.media_object.finished.disconnect(self.loop)
            except Exception as e:
                logger.warning(("Signal disconnect Fail -> %s" % e), level=0)

            try:
                self.video_player.media_object.stateChanged.disconnect(self.video_player_state_changed)
            except Exception as e:
                logger.warning(("Signal disconnect Fail -> %s" % e), level=0)


        self.set_video_player_state(False)

        # Searches the video file
        item = self.lw_video.currentItem()
        candidates = io.get_files(self.current_folder, extensions=self.allowed_extensions, filters=[item.text()])

        # If exists, plays it in the player.
        if candidates:
            video_file = candidates[0]
            self.video_player.clear_urls()
            self.video_player.add_url(video_file)
            self.video_player.set_current_url(0, reset=True)

            self.set_video_player_state(self.video_player.is_ready())

            if self.video_player.is_ready():
                self.lb_playing_name.setText("Playing: %s" % os.path.basename(video_file))
                self.video_player.media_object.finished.connect(self.loop)
                self.video_player.media_object.stateChanged.connect(self.video_player_state_changed)
                self.video_player.play()

    def clear_filters(self):
        """ Clears the filters and updates the ui.
        """
        self.le_filter.setFocus()
        self.le_filter.setText("")
        self.fill_video_list()

    def choose_folder(self):
        """ Uses a dialog to choose the folder and then stores it as the current folder.
        Also calls to fill the ui components with the info in that folder.
        """
        if not self.updating_ui:
            self.updating_ui = True

            # Crates a dialog object to choose folders.
            new_folder_dialog = QtGui.QFileDialog(self)

            # Applies the style.
            theme.apply_style(new_folder_dialog, "video_player.qss")

            # Set the mode to directories
            new_folder_dialog.setFileMode(QtGui.QFileDialog.Directory)
            new_folder_dialog.setOption(QtGui.QFileDialog.ShowDirsOnly, on=True)

            # Shows the dialog and waits for a result. 0 means that has been canceled.
            result = new_folder_dialog.exec_()

            self.updating_ui = False

            # After is closed, uses the given folder to refill the ui with that information.
            if result != 0 and new_folder_dialog.selectedFiles():
                self.current_folder = os.path.abspath(new_folder_dialog.selectedFiles()[0])
                self.update_ui()

    def update_ui(self):
        """ Updates the categories and file list with the videos in the selected folder.
        """
        if not self.updating_ui:
            self.updating_ui = True

            if self.current_folder and os.path.exists(self.current_folder):
                self.le_folder.setText(self.current_folder)

                # Get the categories, that are the subfolders.
                categories = io.get_subfolders(self.current_folder)
                categories = [os.path.abspath(cat) for cat in categories]

                # Sets the new categories in the drop down list.
                self.cbx_categories.clear()
                self.cbx_categories.insertItems(0, categories)

                # Fills the list of videos.
                self.updating_ui = False
                self.fill_video_list()

            self.updating_ui = False

    def fill_video_list(self):
        """ Fills the list of videos availables, using the selected category and the filters.
        """
        if not self.updating_ui:
            self.updating_ui = True

            if self.current_folder and os.path.exists(self.current_folder):
                # Gets all the videos in that category.
                current_category = self.cbx_categories.currentText()
                filters = re.findall(r"[\w']+", self.le_filter.text())
                video_files = io.get_files(current_category, extensions=self.allowed_extensions, filters=filters)
                video_files = [os.path.basename(video_file) for video_file in video_files]
                video_files.sort()

                self.lw_video.clear()
                if video_files:
                    for video_file in video_files:
                        self.lw_video.addItem(os.path.basename(video_file))

            self.updating_ui = False


def ESAPlayerRun():
    # Creates the application
    app = QtGui.QApplication(sys.argv)

    # Applies the theme for the application
    theme.apply_style(app, "video_player.qss")

    # If windows, indicates the process is a separate one to allow the taskbar to use the window icon.
    if os.name == "nt":
        myappid = 'custom.process.esa_player.player' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    # Creates the aplication execution and UI
    execution = ESAPlayer()

    # Enters the application loop
    sys.exit(app.exec_())


def ESAPlayerClose():
    utils.closeTool('ESAPlayer')

#######################################
# execution
if __name__ == "__main__":
    ESAPlayerRun()
