"""Summary"""
#######################################
# imports

import os
import inspect

from PySide import QtCore, QtGui
from PySide.phonon import Phonon

import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.streaming.ui.streaming_ui as streaming_ui

reload(ui)
reload(streaming_ui)

#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def get_streaming_widget(streaming_url):
    # streaming_widget_file = ui.get_ui_file("streaming.ui", get_current_folder(), recursive=True)
    # if streaming_widget_file:
    streaming_widget = streaming_ui.StreamingPlayer(url=streaming_url)

    # print streaming_url
    #
    # streaming_widget.video_player.play(streaming_url)

    return streaming_widget


#######################################
# execution

if __name__ == "__main__":
    streaming_link = "test"
    get_streaming_widget(streaming_link)
    pass
