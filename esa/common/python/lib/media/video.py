"""Summary"""
#######################################
# imports

import os
import inspect

from PySide import QtCore, QtGui

import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.media.video_player as video_player
import esa.common.python.lib.theme.theme as theme

reload(ui)
reload(video_player)
reload(theme)

#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def video_player_widget():
    video_widget = video_player.VideoPlayer()
    return video_widget


#######################################
# execution

if __name__ == "__main__":
    video_link = "test"
    get_video_widget(video_link)
    pass
