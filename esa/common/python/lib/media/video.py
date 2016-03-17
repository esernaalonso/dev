"""Summary"""
#######################################
# imports

import os
import re
import inspect

from PySide import QtCore, QtGui

import esa.common.python.lib.ui.ui as ui
import video_player as video_player
import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.ffmpeg.ffmpeg as ffmpeg

reload(ui)
# reload(video_player)
reload(theme)
reload(ffmpeg)

#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def video_player_widget():
    video_widget = video_player.VideoPlayer()
    return video_widget

def get_video_info(video_file):
    ffmpeg_options = ["-i", video_file]
    return ffmpeg.run(ffmpeg_options, exe_name="ffprobe")

def get_video_frame_rate(video_file):
    video_info = get_video_info(video_file)

    regx = re.compile('.*Video:.*, (.*) fps.*', re.MULTILINE)
    matches = regx.findall(video_info)

    if matches:
        return float(matches[0])
    else:
        return 24

#######################################
# execution

if __name__ == "__main__":
    url = "http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.flv"
    print get_video_info(url)
    print get_video_frame_rate(url)
    pass
