"""Summary"""
#######################################
# imports

import inspect
import os
import re

from PySide import QtGui

import esa.common.python.lib.io.io as io

reload(io)

#######################################
# functionality

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))

def get_current_folder():
    return os.path.dirname(get_current_file())

def get_font_files():
    font_files = io.get_files(get_current_folder(), extensions=[".ttf"], recursive=True)
    return font_files

def get_font_file(name):
    font_files = get_font_files()

    for font_file in font_files:
        if name.replace(".ttf", "") == os.path.basename(font_file).replace(".ttf", ""):
            return font_file

def get_style_files():
    style_files = io.get_files(get_current_folder(), extensions=[".qss"], recursive=True)
    return style_files

def get_style_file(name):
    style_files = get_style_files()

    for style_file in style_files:
        if name.replace(".qss", "") == os.path.basename(style_file).replace(".qss", ""):
            return style_file

def get_style_file_string(style_file):
    with open(style_file, 'r') as open_file:
        style_string = open_file.read().replace('\n', '')
        return style_string

def get_style_file_font_dependencies(style_file):
    font_dependencies = []

    with open(style_file, "r") as f:
        data = f.read()
        f.close()

        regx = re.compile('.*font-family:(.*);.*', re.MULTILINE)
        matches = regx.findall(data)
        if len(matches) > 0:
            for match in matches:
                match = match.lstrip()
                if match != "":
                    font_dependency = get_font_file(str(match))
                    if font_dependency:
                        font_dependencies.append(font_dependency)

    return font_dependencies

def load_font(font_file):
    if os.path.exists(font_file):
        return QtGui.QFontDatabase.addApplicationFont(font_file)

def apply_style(application, style_name):
    style_file = get_style_file(style_name)

    if style_file:
        font_dependencies = get_style_file_font_dependencies(style_file)
        for font_file in font_dependencies:
            load_font(font_file)

        style_string = get_style_file_string(style_file)
        application.setStyleSheet(style_string)

#######################################
# execution

if __name__ == "__main__":
    # the_folder = "P:\\dev\\esa\\common\\python\\lib\\theme\\styles\\"
    # files = get_style_files(the_folder)
    # for file in files:
    #     style_string = get_style_file_string(file)
    #     print style_string
    pass
