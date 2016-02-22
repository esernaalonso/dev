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
    return io.get_files(folder, extensions=[".png", ".jpg"], recursive=recursive)


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

#######################################
# execution

if __name__ == "__main__":
    pass
