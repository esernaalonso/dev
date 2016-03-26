"""Summary"""
#######################################
# imports

import os
from PySide import QtGui

import esa.common.python.lib.io.io as io

reload(io)

#######################################
# functionality


def get_image_files(folder, recursive=True):
    return io.get_files(folder, extensions=[".png", ".jpg", ".gif"], recursive=recursive)


def get_image_file(name, folder, recursive=True):
    image_files = get_image_files(folder, recursive=recursive)

    for image_file in image_files:
        short_name = os.path.basename(os.path.splitext(name)[0])
        file_base_name = os.path.basename(os.path.splitext(image_file)[0])
        if short_name == file_base_name:
            return image_file


def create_pixmap(source_image):
    if os.path.exists(source_image):
        return QtGui.QPixmap(source_image)


def create_icon(source_image):
    if os.path.exists(source_image):
        return QtGui.QIcon(source_image)


def create_movie(source_image):
    if os.path.exists(source_image):
        return QtGui.QMovie(source_image)

#######################################
# execution

if __name__ == "__main__":
    # folder = "P:/dev/esa/common/python/lib/media/ui/icons"
    # files = get_image_files(folder)
    # print files
    # image_files = get_image_file("loading.gif", folder)
    # print image_files
    pass
