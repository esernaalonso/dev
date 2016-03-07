import mpylayer
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.container = QtGui.QWidget(self)
        self.container.setStyleSheet('background: black')
        self.button = QtGui.QPushButton('Open', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.addWidget(self.button)
        self.mplayer = mpylayer.MPlayerControl()

    def handleButton(self):
        path = QtGui.QFileDialog.getOpenFileName()
        # if not path.isEmpty():
        #     self.mplayer.loadfile(unicode(path))

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
