from PySide import QtCore, QtGui

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.edit = QtGui.QTextEdit(self)
        self.edit.installEventFilter(self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.edit)

    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            widget is self.edit):
            key = event.key()
            if key == QtCore.Qt.Key_Left:
                print('LEFT')
            else:
                if key == QtCore.Qt.Key_Return:
                    self.edit.setText('return')
                elif key == QtCore.Qt.Key_Enter:
                    self.edit.setText('enter')
                return True
        return QtGui.QWidget.eventFilter(self, widget, event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 300, 300)
    window.show()
    sys.exit(app.exec_())
