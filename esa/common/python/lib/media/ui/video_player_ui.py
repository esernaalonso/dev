from PySide import QtCore, QtGui
from PySide import phonon

import os
import sys
import inspect

import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.image.image as image
import esa.common.python.lib.ui.ui as ui

reload(theme)
reload(ui)
reload(image)

class Overlay(QtGui.QLabel):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)

        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setText("OVERLAY TEXT")

        # palette = QtGui.QPalette(self.palette())
        # palette.setColor(palette.Background, QtCore.Qt.transparent)

        # self.setPalette(palette)

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setStyleSheet("background:transparent;")

    # def paintEvent(self, event):
    #     painter = QtGui.QPainter()
    #     painter.begin(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(255, 255, 255, 127)))
    #     painter.drawLine(self.width()/8, self.height()/8, 7*self.width()/8, 7*self.height()/8)
    #     painter.drawLine(self.width()/8, 7*self.height()/8, 7*self.width()/8, self.height()/8)
    #     painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

class VideoPlayerFullScreen(QtGui.QWidget):
    def __init__(self, video_player_widget=None):
        super(VideoPlayerFullScreen, self).__init__()
        self.video_player_widget = video_player_widget
        self.initUI()

    def initUI(self):
        self.setObjectName("VideoPlayerFullScreen")

        # Applies the theme for the widget
        # theme.apply_style(self, "video_player.qss")

        # Allows full screen
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.setMinimumSize(500, 500)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        if self.video_player_widget:
            self.layout().addWidget(self.video_player_widget)


class VideoPlayer(QtGui.QWidget):
    def __init__(self, url=None):
        super(VideoPlayer, self).__init__()

        self.is_full_screen = False
        self.normal_mode_parent = None

        self.initUI()

    def get_current_file(self):
        return os.path.abspath(inspect.getsourcefile(lambda:0))

    def get_current_folder(self):
        return os.path.dirname(self.get_current_file())

    def initUI(self):
        self.setObjectName("VideoPlayer")

        # Applies the theme for the widget
        theme.apply_style(self, "video_player.qss")

        # Allows full screen
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        # Inserts the .ui content
        video_player_ui_file = ui.get_ui_file("video_player.ui", self.get_current_folder())
        self.ui = ui.loadUiWidget(video_player_ui_file, parent=self)

        # Layout.
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Watermark widget
        # self.graphics_scene = QtGui.QGraphicsScene()
        # self.watermark_text = self.graphics_scene.addText("THIS IS A WATERMARK")
        #
        # self.lb_watermark = QtGui.QLabel()
        # self.lb_watermark.setText("THIS IS A WATERMARK")
        # self.lb_watermark.setStyleSheet("background: transparent;")

        # Phonon components to manage a video.

        # Video Player
        self.video_player = phonon.Phonon.VideoPlayer(self)
        self.video_player_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.video_player_size_policy.setHorizontalStretch(0)
        self.video_player_size_policy.setVerticalStretch(0)
        self.video_player_size_policy.setHeightForWidth(self.video_player.sizePolicy().hasHeightForWidth())
        self.video_player.setSizePolicy(self.video_player_size_policy)
        self.video_player.setObjectName("video_player")

        # self.lb_watermark.setParent(self.video_player)
        # self.graphics_scene.setParent(self.video_player)
        # self.watermark_text.setPos(150, 150)

        # Seek Slider - timeline
        self.seek_slider = phonon.Phonon.SeekSlider(self)
        self.seek_slider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.seek_slider.setObjectName("seek_slider")

        # Volume Slider.
        self.volume_slider = phonon.Phonon.VolumeSlider(self)
        self.volume_slider.setMaximumSize(QtCore.QSize(150, 20))
        self.volume_slider.setMuteVisible(False)
        self.volume_slider.setObjectName("volume_slider")

        # Watermark.
        self.overlay = Overlay(self)

        # self.sbt_watermark = phonon.Phonon.SubtitleDescription()
        # self.media_controller = None

        # Inserts the phonon components in the widget containers prepared for them.
        ui.insert_widget(self, "wg_video", self.video_player, None)
        ui.insert_widget(self, "wg_seek", self.seek_slider, None)
        ui.insert_widget(self, "wg_volume", self.volume_slider, None)

        # Stores controls to use with signals and/or to get values in process.
        self.pb_refresh = ui.get_child(self, "pb_refresh")
        self.pb_play_prev = ui.get_child(self, "pb_play_prev")
        self.pb_play_decrease = ui.get_child(self, "pb_play_decrease")
        self.pb_play_inverse = ui.get_child(self, "pb_play_inverse")
        self.pb_play = ui.get_child(self, "pb_play")
        self.pb_play_increase = ui.get_child(self, "pb_play_increase")
        self.pb_play_next = ui.get_child(self, "pb_play_next")
        self.pb_volume_down = ui.get_child(self, "pb_volume_down")
        self.pb_volume_up = ui.get_child(self, "pb_volume_up")
        self.pb_volume_on = ui.get_child(self, "pb_volume_on")
        self.pb_expand = ui.get_child(self, "pb_expand")

        # Load the ui icons.
        self.refresh_icon = image.get_image_file("refresh.png", self.get_current_folder())
        self.play_prev_icon = image.get_image_file("play_prev.png", self.get_current_folder())
        self.play_decrease_icon = image.get_image_file("play_decrease.png", self.get_current_folder())
        self.play_inverse_icon = image.get_image_file("play_inverse.png", self.get_current_folder())
        self.play_icon = image.get_image_file("play.png", self.get_current_folder())
        self.pause_icon = image.get_image_file("pause.png", self.get_current_folder())
        self.play_increase_icon = image.get_image_file("play_increase.png", self.get_current_folder())
        self.play_next_icon = image.get_image_file("play_next.png", self.get_current_folder())
        self.volume_up_icon = image.get_image_file("volume_up.png", self.get_current_folder())
        self.volume_down_icon = image.get_image_file("volume_down.png", self.get_current_folder())
        self.volume_on_icon = image.get_image_file("volume_on.png", self.get_current_folder())
        self.volume_off_icon = image.get_image_file("volume_off.png", self.get_current_folder())
        self.expand_icon = image.get_image_file("expand.png", self.get_current_folder())
        self.reduce_icon = image.get_image_file("reduce.png", self.get_current_folder())

        # Applies the icons.
        self.pb_refresh.setIcon(image.create_pixmap(self.refresh_icon))
        self.pb_play_prev.setIcon(image.create_pixmap(self.play_prev_icon))
        self.pb_play_decrease.setIcon(image.create_pixmap(self.play_decrease_icon))
        self.pb_play_inverse.setIcon(image.create_pixmap(self.play_inverse_icon))
        self.pb_play.setIcon(image.create_pixmap(self.play_icon))
        self.pb_play_increase.setIcon(image.create_pixmap(self.play_increase_icon))
        self.pb_play_next.setIcon(image.create_pixmap(self.play_next_icon))
        self.pb_volume_down.setIcon(image.create_pixmap(self.volume_down_icon))
        self.pb_volume_up.setIcon(image.create_pixmap(self.volume_up_icon))
        self.pb_volume_on.setIcon(image.create_pixmap(self.volume_on_icon))
        self.pb_expand.setIcon(image.create_pixmap(self.expand_icon))

        # Creates the signals
        self.pb_play.clicked.connect(self.toggle_play)
        self.pb_expand.clicked.connect(self.toggle_full_screen)

    def set_url(self, url):
        if url:
            self.video_player.play(url)
            self.video_player.pause()

            self.seek_slider.setMediaObject(self.video_player.mediaObject())
            self.volume_slider.setAudioOutput(self.video_player.audioOutput())

            # self.media_controller = phonon.Phonon.MediaController(self.video_player.mediaObject())
            # subtitle_file = os.path.join(self.get_current_folder(), "test_subtitle.srt")
            # self.media_controller.loadSubtitleFile(subtitle_file)
            # test_subtitle = phonon.Phonon.SubtitleDescription(1, {"file":subtitle_file})
            # print test_subtitle.propertyNames()
            # print test_subtitle.index()
            # print test_subtitle.isValid()
            # print test_subtitle.property("file")
            # print test_subtitle.description()
            # print test_subtitle.name()
            # test_subtitle.name = os.path.join(self.get_current_folder(), "test_subtitle.srt")
            # self.media_controller.setCurrentSubtitle(test_subtitle)
            # print self.media_controller.currentSubtitle()
            # print self.media_controller.availableSubtitles()

    def toggle_play(self):
        if self.video_player.mediaObject():
            if self.video_player.isPlaying():
                self.pause()
            else:
                self.play()

    def play(self):
        if self.video_player.mediaObject():
            self.video_player.play()
            self.pb_play.setIcon(image.create_pixmap(self.pause_icon))

    def pause(self):
        if self.video_player.mediaObject():
            self.video_player.pause()
            self.pb_play.setIcon(image.create_pixmap(self.play_icon))

    def toggle_full_screen(self):
        if not self.is_full_screen:
            self.enter_full_screen()
        else:
            self.exit_full_screen()

    def enter_full_screen(self):
        self.normal_mode_parent = self.parent()
        self.is_full_screen = True
        self.video_player_full_screen = VideoPlayerFullScreen(video_player_widget=self)
        self.video_player_full_screen.showFullScreen()

    def exit_full_screen(self):
        self.normal_mode_parent.layout().addWidget(self)
        self.is_full_screen = False
        self.video_player_full_screen.close()
