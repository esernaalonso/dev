"""Summary"""
#######################################
# imports

import os
import inspect

from PySide import QtCore, QtGui
from PySide.phonon import Phonon

import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.media.ui.video_player_ui as video_player_ui
import esa.common.python.lib.theme.theme as theme

reload(ui)
reload(video_player_ui)
reload(theme)

#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def get_video_player(video_url):
    video_widget = video_player_ui.VideoPlayer(url=video_url)
    return video_widget


#######################################
# execution

if __name__ == "__main__":
    video_link = "test"
    get_video_widget(video_link)
    pass
