"""Summary"""
#######################################
# imports

from PySide import QtCore, QtGui

import esa.common.python.lib.ui.ui as ui

reload(ui)

#######################################
# functionality


def get_streaming_widget(streaming_link):
    # streaming_widget = None
    streaming_widget = QtGui.QTextBrowser()

    text = """
        <html>
        <style type="text/css">
            p {color: red}
            div {color: blue}
        </style>
        <body>
        <p>This is  a paragraph</p>
        <div>This is inside div element</div>
        </body>
        </html>
    """

    streaming_widget.setHtml(text)

    return streaming_widget


#######################################
# execution

if __name__ == "__main__":
    streaming_link = "test"
    get_streaming_widget(streaming_link)
    pass
