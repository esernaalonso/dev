"""Summary"""
#######################################
# imports

import os
import re
import json
import inspect

from PySide import QtCore, QtGui

import esa.common.python.lib.ui.ui as ui
import esa.common.python.lib.theme.theme as theme
import esa.common.python.lib.ffmpeg.ffmpeg as ffmpeg
import esa.common.python.lib.logger.logger as logger


#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def get_video_extensions():
    return [".avi", ".flv", ".mkv", ".mp4", ".mov"]


def get_video_info(video_file, json_format=True):
    # ffmpeg_options = ["-i", video_file]
    ffmpeg_options = ["-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_file]
    video_info = ffmpeg.run(ffmpeg_options, exe_name="ffprobe.exe")
    if json_format:
        try:
            video_info = json.loads(video_info)
        except Exception as e:
            logger.warning(("Error Parsing Video Info -> %s" % e), level=0)
            return None

    return video_info


def get_video_frame_rate(video_file):
    video_info = get_video_info(video_file, json_format=True)

    if video_info:
        for stream in video_info["streams"]:
            if stream["codec_type"] == "video":
                frame_rate = float(stream["r_frame_rate"].split("/")[0]) / float(stream["r_frame_rate"].split("/")[1])
                return frame_rate

    return 24.0


def get_video_size(video_file):
    video_info = get_video_info(video_file, json_format=True)

    if video_info:
        for stream in video_info["streams"]:
            if stream["codec_type"] == "video":
                size = {"width": int(stream["width"]), "height": int(stream["height"])}
                return size


def encode_for_streaming(video_file, scales=["full"]):
    """ Encodes the given video using ffmpeg for streaming purposes.

        Args:
            scales (list of strings, optional): Sizes to encode. Allowed values - "full", "half", "third", "quarter"
    """
    allowed_scales = {"full": 1.0, "threequarters": 0.75, "twothirds":(2.0/3.0), "half": 0.5, "third": (1.0/3.0), "quarter": 0.25}

    if video_file:
        video_size = get_video_size(video_file)
        if video_size:
            for scale in scales:
                if scale in allowed_scales:
                    new_width = int(video_size["width"]*allowed_scales[scale])
                    new_height = int(video_size["height"]*allowed_scales[scale])

                    new_width = new_width if new_width % 2 == 0 else new_width + 1
                    new_height = new_height if new_height % 2 == 0 else new_height + 1

                    new_video_file = "%s_%s.mp4" % (os.path.splitext(video_file)[0], scale)
                    ffmpeg_options = ["-i", video_file, "-c:a", "aac", "-strict", "-2", "-b:a", "128k", "-c:v", "libx264", "-profile:v", "baseline", "-filter:v", ("scale=%s:%s" % (new_width, new_height)), new_video_file]

                    result = ffmpeg.run(ffmpeg_options, exe_name="ffmpeg.exe")

                    logger.info(("Encoded video -> %s" % new_video_file), level=0)
                    logger.info(("Result: %s" % result), level=1)
        else:
            logger.error(("Error getting the original video size -> %s" % video_file), level=0)


#######################################
# execution

if __name__ == "__main__":
    # url = "http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.mp4"
    url = "P:/insideAnim/educ/masters/animation/05_creatures/01_creatures_workshop/video/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.flv"
    # print get_video_info(url)
    # print get_video_frame_rate(url)
    # print get_video_size(url)

    # ffmpeg_options = ["-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", url]
    # result = ffmpeg.run(ffmpeg_options, exe_name="ffprobe.exe")
    # print result

    # encode_for_streaming(url, scales=["full", "half", "third", "quarter"])
    # encode_for_streaming(url, scales=["half", "third"])
    # encode_for_streaming(url, scales=["quarter"])
    # encode_for_streaming(url, scales=["twothirds"])
    encode_for_streaming(url, scales=["threequarters"])

    pass
