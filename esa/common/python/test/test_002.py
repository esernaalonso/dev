# based: https://github.com/baudm/mplayer.py/blob/master/mplayer/qt4.py

import sys
import os
import time
from subprocess import PIPE

from mplayer.core import Player
from mplayer import misc

try:
    from PySide.QtGui import QX11EmbedContainer as _Container
except ImportError as e:
    from PySide.QtGui import QWidget as _Container

from PySide import QtCore, QtGui
# thanks: http://qt-project.org/wiki/Signals_and_Slots_in_PySide_Japanese
QtCore.pyqtSignal = QtCore.Signal
QtCore.pyqtSlot = QtCore.Slot

__all__ = ['QtPlayer', 'QPlayerView']

class QtPlayer(Player):
    def __init__(self, args=(), stdout=PIPE, stderr=None, autospawn=True):
        super(QtPlayer, self).__init__(args, autospawn=False)
        self._stdout = _StdoutWrapper(handle=stdout)
        self._stderr = _StderrWrapper(handle=stderr)
        if autospawn: self.spawn()

class QPlayerView(QtGui.QWidget):
    eof = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, args=(), stderr=None):
        super(QPlayerView, self).__init__(parent)
        # self._player = QtPlayer(('-msglevel', 'global=6', '-fixed-vo', '-fs', '-volume', 10,
                                #  '-wid', int(self.winId())) + args, stderr=stderr)
        self._player = QtPlayer(('-msglevel', 'global=6', '-fixed-vo', '-fs', '-volume', 10,
                                 '-wid', 1) + args, stderr=stderr)
        self._player.stdout.connect(self._handle_data)
        self.destroyed.connect(self._on_destroy)
        self._build_gui()

    @property
    def player(self):
        return self._player

    def _on_destroy(self):
        self._player.quit()

    def _handle_data(self, data):
        if data.startswith('EOF code:'):
            code = data.partition(':')[2].strip()
            self.eof.emit(int(code))

    def resizeEvent(self, event):
        pass

    def _load_clicked(self):
        self.resize(640,480)
        self._player.loadfile("C:/tmp/creatures01_lsn01_sbt02_animal_anatomy_vs_human_anatomy.flv")

    def _pause_clicked(self):
        self._player.pause()

    def _vol_plusone_clicked(self):
        vol = self._player.volume
        if vol != None:
            vol_limit = int(vol + 1)
            self._player.volume = vol_limit
            print('Volume: %s' % vol_limit)

    def _vol_minusone_clicked(self):
        vol = self._player.volume
        if vol != None:
            vol_limit = int(vol - 1)
            self._player.volume = vol_limit
            print('Volume: %s' % vol_limit)

    def _build_gui(self):
        self._load_button = QtGui.QPushButton("Load Files")
        self._load_button.clicked.connect(self._load_clicked)
        self._load_button.show()

        self._pause_button = QtGui.QPushButton("Play/Pause")
        self._pause_button.clicked.connect(self._pause_clicked)
        self._pause_button.show()

        self._vol_plusone_button = QtGui.QPushButton("Vol+")
        self._vol_plusone_button.clicked.connect(self._vol_plusone_clicked)
        self._vol_plusone_button.show()

        self._vol_minusone_button = QtGui.QPushButton("Vol-")
        self._vol_minusone_button.clicked.connect(self._vol_minusone_clicked)
        self._vol_minusone_button.show()

class _StderrWrapper(misc._StderrWrapper):

    def __init__(self, **kwargs):
        super(_StderrWrapper, self).__init__(**kwargs)
        self._notifier = None

    def _attach(self, source):
        super(_StderrWrapper, self)._attach(source)
        self._notifier = QtCore.QSocketNotifier(self._source.fileno(),
                                                QtCore.QSocketNotifier.Read)
        self._notifier.activated.connect(self._process_output)

    def _detach(self):
        self._notifier.setEnabled(False)
        super(_StderrWrapper, self)._detach()

class _StdoutWrapper(_StderrWrapper, misc._StdoutWrapper):
    pass

class MainForm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

    def resizeEvent(self, event):
        print(self.width())
        print(self.height())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = MainForm()
    w.resize(640, 480)
    w.setWindowTitle('QtPlayer')
    v = QPlayerView(w)
    v.eof.connect(app.closeAllWindows)
    w.show()
    #v.player.loadfile(sys.argv[1])
    #print(dir(v.player))
    #v.player.loadfile("/home/renax/src/QpcyPie/testsdata/test_video.mp4")
    sys.exit(app.exec_())
