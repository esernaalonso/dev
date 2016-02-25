import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide.QtGui import *
from PySide.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setGeometry(100, 100, 640, 480)
        showButton = QPushButton('Show')

        toolbarShowButton = self.addToolBar('Show button toolbar')

        toolbarShowButton.addWidget(showButton)
        self.connect(showButton, SIGNAL('clicked()'), self.showButtonClicked)

        # dummy QWidget
        tempWidget = QWidget()
        self.setCentralWidget(tempWidget)

    def showButtonClicked(self):

        width = self.centralWidget().width()
        height = self.centralWidget().height()

        # convert to float (python 2) to prevent
        # flooring in the following divisions
        dpi = float(100)

        # create the canvas and replace the central widget
        self.graphLabel = GraphCanvas(self, width=width/dpi, height=height/dpi, dpi=dpi);
        self.setCentralWidget(self.graphLabel)

        self.graphLabel.drawGraph()

class GraphCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.background = None

    def drawGraph(self):
        self.axes.cla()
        self.someplot = self.axes.plot(range(1,5), range(1,5))
        self.redVert, = self.axes.plot(None, None, 'r--')
        self.greenVert, = self.axes.plot(None, None, 'g--')
        self.yellowVert, = self.axes.plot(None, None, 'y--')

        self.verticalLines = (self.redVert, self.greenVert, self.yellowVert)

        self.fig.canvas.mpl_connect('motion_notify_event', self.onMove)

        self.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)

    def onMove(self, event):

        # cursor moves on the canvas
        if event.inaxes:

            # restore the clean background
            self.fig.canvas.restore_region(self.background)
            ymin, ymax = self.axes.get_ylim()
            x = event.xdata - 1

            # draw each vertical line
            for line in self.verticalLines:
                line.set_xdata((x,))
                line.set_ydata((ymin, ymax))
                self.axes.draw_artist(line)
                x += 1

            self.fig.canvas.blit(self.axes.bbox)

    def setFig(self):
        '''
        Draws the canvas again after the main window
        has been resized.
        '''

        try:
            # hide all vertical lines
            for line in self.verticalLines:
                line.set_visible(False)

        except AttributeError:
            pass

        else:
            # draw canvas again and capture the background
            self.draw()
            self.background = self.fig.canvas.copy_from_bbox(self.axes.bbox)

            # set all vertical lines visible again
            for line in self.verticalLines:
                line.set_visible(True)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__': main()
