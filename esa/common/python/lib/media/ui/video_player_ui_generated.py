# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P:/dev/esa/common/python/lib/streaming/ui/streaming.ui'
#
# Created: Fri Mar 04 18:53:55 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 505)
        Form.setMinimumSize(QtCore.QSize(640, 505))
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setAutoFillBackground(False)
        Form.setStyleSheet("QWidget\n"
"{\n"
"    font-family: Comfortaa;\n"
"    font-size: 13px;\n"
"    color: #e1e1e1;\n"
"    background-color: #222222;\n"
"    selection-background-color:#5d5d5d;\n"
"    selection-color: black;\n"
"    background-clip: border;\n"
"    border-image: none;\n"
"    outline: 0;\n"
"}")
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.videoPlayer = phonon.Phonon.VideoPlayer(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoPlayer.sizePolicy().hasHeightForWidth())
        self.videoPlayer.setSizePolicy(sizePolicy)
        self.videoPlayer.setMinimumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(-1)
        self.videoPlayer.setFont(font)
        self.videoPlayer.setObjectName("videoPlayer")
        self.gridLayout.addWidget(self.videoPlayer, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(3, -1, 3, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.seekSlider = phonon.Phonon.SeekSlider(Form)
        self.seekSlider.setMaximumSize(QtCore.QSize(16777215, 20))
        self.seekSlider.setIconVisible(False)
        self.seekSlider.setObjectName("seekSlider")
        self.horizontalLayout.addWidget(self.seekSlider)
        self.volumeSlider = phonon.Phonon.VolumeSlider(Form)
        self.volumeSlider.setMaximumSize(QtCore.QSize(150, 20))
        font = QtGui.QFont()
        font.setFamily("Comfortaa")
        font.setPointSize(-1)
        self.volumeSlider.setFont(font)
        self.volumeSlider.setAutoFillBackground(False)
        self.volumeSlider.setTracking(True)
        self.volumeSlider.setMuteVisible(True)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout.addWidget(self.volumeSlider)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Play", None, QtGui.QApplication.UnicodeUTF8))

from PySide import phonon
