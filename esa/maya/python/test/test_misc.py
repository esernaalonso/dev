import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWebKit import QWebView

app = QApplication(sys.argv)
web = QWebView()
web.showFullScreen()
web.load(QUrl("http://www.google.com"))
sys.exit(app.exec_())
