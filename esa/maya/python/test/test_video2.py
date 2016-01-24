from PySide import QtGui, QtCore
from PySide.phonon import Phonon


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Video Player')
        self.media = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget(self)
        self.video.setMinimumSize(400, 400)
        self.audio = Phonon.AudioOutput(Phonon.VideoCategory, self)
        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)
        self.buttonChoose = QtGui.QPushButton('Choose File', self)
        self.buttonMimes = QtGui.QPushButton('Show Mimetypes', self)
        self.slider = Phonon.VolumeSlider(self)
        self.slider.setAudioOutput(self.audio)
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.video, 0, 0, 1, 2)
        layout.addWidget(self.buttonChoose, 1, 0)
        layout.addWidget(self.buttonMimes, 1, 1)
        layout.addWidget(self.slider, 2, 0, 1, 2)
        layout.setRowStretch(0, 1)
        self.media.stateChanged.connect(self.handleStateChanged)
        self.buttonChoose.clicked.connect(self.handleButtonChoose)
        self.buttonMimes.clicked.connect(self.handleButtonMimes)

    def handleButtonChoose(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            dialog = QtGui.QFileDialog(self)
            dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                path = dialog.selectedFiles()[0]
                self.media.setCurrentSource(Phonon.MediaSource(path))
                self.media.play()
            dialog.deleteLater()

    def handleButtonMimes(self):
        dialog = MimeDialog(self)
        dialog.exec_()

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.buttonChoose.setText('Stop')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.buttonChoose.setText('Choose File')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play: %s' % source)
                print ('  %s' % self.media.errorString())


class MimeDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Mimetypes')
        listbox = QtGui.QListWidget(self)
        listbox.setSortingEnabled(True)
        backend = Phonon.BackendCapabilities
        listbox.addItems(backend.availableMimeTypes())
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(listbox)
        self.resize(300, 500)


if __name__ == '__main__':
    import sys
    # app = QtGui.QApplication(sys.argv)
    # app.setApplicationName('Phonon Player')
    window = Window()
    window.show()
    # sys.exit(app.exec_())
