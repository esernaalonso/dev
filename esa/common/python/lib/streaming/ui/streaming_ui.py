from PySide import QtCore, QtGui
from PySide import phonon

class StreamingPlayer(QtGui.QWidget):
    def __init__(self, url=None):
        super(StreamingPlayer, self).__init__()
        self.initUI()
        if url:
            self.set_url(url)

    def initUI(self):
        self.setObjectName("StreamingPlayer")
        self.setStyleSheet("QLayout{ border: 1px solid #3A3939; border-radius: 2px;}")

        self.resize(640, 505)
        self.setMinimumSize(QtCore.QSize(640, 505))

        self.grid_layout = QtGui.QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(3)
        self.grid_layout.setObjectName("grid_layout")

        self.video_player = phonon.Phonon.VideoPlayer(self)
        self.video_player_size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.video_player_size_policy.setHorizontalStretch(0)
        self.video_player_size_policy.setVerticalStretch(0)
        self.video_player_size_policy.setHeightForWidth(self.video_player.sizePolicy().hasHeightForWidth())
        self.video_player.setSizePolicy(self.video_player_size_policy)
        self.video_player.setMinimumSize(QtCore.QSize(640, 480))
        self.video_player.setObjectName("video_player")

        self.grid_layout.addWidget(self.video_player, 0, 0, 1, 1)

        self.horizontal_layout = QtGui.QHBoxLayout()
        self.horizontal_layout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontal_layout.setContentsMargins(3, -1, 3, -1)
        self.horizontal_layout.setObjectName("horizontal_layout")

        self.pb_play = QtGui.QPushButton(self)
        self.pb_play.setMaximumSize(QtCore.QSize(20, 20))
        self.pb_play.setObjectName("pb_play")

        self.horizontal_layout.addWidget(self.pb_play)

        self.seek_slider = phonon.Phonon.SeekSlider(self)
        self.seek_slider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.seek_slider.setObjectName("seek_slider")

        self.horizontal_layout.addWidget(self.seek_slider)

        self.volume_slider = phonon.Phonon.VolumeSlider(self)
        self.volume_slider.setMaximumSize(QtCore.QSize(150, 20))
        self.volume_slider.setObjectName("volume_slider")

        self.horizontal_layout.addWidget(self.volume_slider)

        self.grid_layout.addLayout(self.horizontal_layout, 1, 0, 1, 1)


    def set_url(self, url):
        if url:
            self.video_player.play(url)
            self.seek_slider.setMediaObject(self.video_player.mediaObject())
            self.volume_slider.setAudioOutput(self.video_player.audioOutput())
