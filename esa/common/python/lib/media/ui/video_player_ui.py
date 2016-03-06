from PySide import QtCore, QtGui
from PySide import phonon

import os
import inspect

import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.ui.ui as ui

reload(theme)
reload(ui)

class VideoPlayer(QtGui.QWidget):
    def __init__(self, url=None):
        super(VideoPlayer, self).__init__()
        self.initUI()
        if url:
            self.set_url(url)

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initUI(self):
        self.setObjectName("VideoPlayer")

        # Applies the theme for the widget
        theme.apply_style(self, "video_player.qss")

        # Inserts the .ui content
        video_player_ui_file = ui.get_ui_file("video_player.ui", self.get_current_folder())
        self.ui = ui.loadUiWidget(video_player_ui_file, parent=self)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Phonon components to manage a video.
        self.video_player = phonon.Phonon.VideoPlayer(self)
        self.video_player_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.video_player_size_policy.setHorizontalStretch(0)
        self.video_player_size_policy.setVerticalStretch(0)
        self.video_player_size_policy.setHeightForWidth(self.video_player.sizePolicy().hasHeightForWidth())
        self.video_player.setSizePolicy(self.video_player_size_policy)
        # self.video_player.setMinimumSize(QtCore.QSize(640, 360))
        self.video_player.setObjectName("video_player")

        self.seek_slider = phonon.Phonon.SeekSlider(self)
        self.seek_slider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.seek_slider.setObjectName("seek_slider")

        self.volume_slider = phonon.Phonon.VolumeSlider(self)
        self.volume_slider.setMaximumSize(QtCore.QSize(150, 20))
        self.volume_slider.setObjectName("volume_slider")

        # Inserts the phonon components in the widget containers prepared for them.
        ui.insert_widget(self, "wg_video", self.video_player, None)
        ui.insert_widget(self, "wg_seek", self.seek_slider, None)
        ui.insert_widget(self, "wg_volume", self.volume_slider, None)

        # Stores controls to use with signals and/or to get values in process.
        self.pb_play = ui.get_child(self, "pb_play")

        # Creates the signals
        self.pb_play.clicked.connect(self.toggle_play)

    def set_url(self, url):
        if url:
            self.video_player.play(url)
            self.video_player.pause()
            self.seek_slider.setMediaObject(self.video_player.mediaObject())
            self.volume_slider.setAudioOutput(self.video_player.audioOutput())

    def toggle_play(self):
        if self.video_player.mediaObject():
            if self.video_player.isPlaying():
                self.pause()
            else:
                self.play()

    def play(self):
        if self.video_player.mediaObject():
            self.video_player.play()

    def pause(self):
        if self.video_player.mediaObject():
            self.video_player.pause()
