"""Summary"""
#######################################
# imports

import os

import esa.common.python.lib.io.io as io

reload(io)

#######################################
# functionality

def get_style_files(folder_path):
    style_files = io.get_files(folder_path, extensions=[".stylesheet"], recursive=True)
    return style_files

def get_style_file(name, folder_path):
    style_files = get_style_files(folder_path)

    for style_file in style_files:
        if name == os.path.basename(style_file).replace(".stylesheet", ""):
            return style_file

def get_style_file_string(style_file):
    with open(style_file, 'r') as open_file:
        style_string = open_file.read().replace('\n', '')
        return style_string

#######################################
# execution

if __name__ == "__main__":
    the_folder = "P:\\dev\\esa\\common\\python\\lib\\theme\\styles\\"
    files = get_style_files(the_folder)
    for file in files:
        style_string = get_style_file_string(file)
        print style_string
    pass
