#######################################
# imports

# import maya.cmds as cmds
# import maya.OpenMayaUI as apiUI
import sys
import os

from PySide import QtCore, QtGui
# from PySide.phonon import Phonon
from PySide.QtWebKit import QWebView

import esa.maya.python.lib.utils as utils
import esa.maya.python.lib.ui as ui

reload(utils)
reload(ui)

#######################################
# attributes

permission = "developer"

#######################################
# functionality


class VideoPlayer(QtGui.QDialog):
    def __init__(self,  parent=utils.getMayaWindow()):
        super(VideoPlayer, self).__init__(parent)

        self.setObjectName('VideoPlayer')
        self.opened = True

        self.initUI()

    def initUI(self):
        # layout
        self.setLayout(QtGui.QVBoxLayout())

        # add main widget
        self.mainWiget = VideoPlayerMainWidget()
        self.layout().addWidget(self.mainWiget)
        self.layout().setSpacing(0)

        self.show()

    def closeEvent(self, event):
        self.opened = False


class VideoPlayerMainWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(VideoPlayerMainWidget, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)

        self.ui = ui.loadUiWidgetFromPyFile(__file__, parent=self)

        # layout
        self.setLayout(QtGui.QVBoxLayout())
        # self.layout().addWidget(self.ui)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(2, 2, 2, 2)

        # self.vp_main_video = ui.get_child(self.ui, "vp_main_video")

        self.init_video()

    def init_video(self):
        web = QWebView()
        web.showFullScreen()
        web.load(QUrl("http://www.google.com"))
        self.layout().addWidget(web)

        # file_path = "P:/insideAnim/educ/masters/animation/05_creatures/01_creatures_workshop/video/creatures_tiger_walk_steps_up_hss_002.mp4"
        # media_src = Phonon.MediaSource(file_path)

        # media_obj = Phonon.MediaObject()
        # media_obj.setCurrentSource(media_src)

        # for prop in dir (self.vp_main_video):
        #     print prop

        # video_widget = Phonon.VideoWidget()
        # self.layout().addWidget(video_widget)
        #
        # audio_out = Phonon.AudioOutput(Phonon.VideoCategory)

        # Phonon.createPath(media_obj, audio_out)
        # Phonon.createPath(media_obj, self.vp_main_video)

        # self.widget = video_widget
        #
        # video_widget.show()
        # media_obj.play()
        # video_widget.resize(500, 400)
        #
        # print video_widget

        # file_path = "P:/insideAnim/educ/masters/animation/05_creatures/01_creatures_workshop/video/creatures_tiger_walk_steps_up_hss_002.mp4"
        # m_media = Phonon.MediaObject()
        # output = Phonon.AudioOutput(Phonon.MusicCategory)
        # Phonon.createPath(m_media, output)
        # m_media.setCurrentSource(Phonon.MediaSource(file_path))
        # m_media.play()
        # # m_media.resize(500, 400)

        # self.vp_main_video.mediaObject().setCurrentSource(media_src)

        # url = QtCore.QUrl("http://www.campus.insideanim.com/wp-content/uploads/tmp/creatures_tiger_walk_cycle_hss_001_user_.mp4")
        # self.vp_main_video.mediaObject().setCurrentSource(url)
        # url = "http://www.campus.insideanim.com/wp-content/uploads/tmp/creatures_tiger_walk_cycle_hss_001_user_.mp4"
        # self.vp_main_video.play(url)

        # self.vp_main_video.mediaObject().play()
        # self.vp_main_video.play()
        # print self.vp_main_video.mediaObject().hasVideo()
        #
        # print self.vp_main_video.mediaObject().currentSource().fileName()
        # print self.vp_main_video.mediaObject().currentSource().url()
        # print "---------------------------------"


def VideoPlayerRun():
    utils.closeTool('VideoPlayer')
    dTool = VideoPlayer()


def VideoPlayerClose():
    utils.closeTool('VideoPlayer')

#######################################
# execution
if __name__ == "__main__":
    VideoPlayerRun()
