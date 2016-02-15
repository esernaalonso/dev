"""Summary"""
############################################################################################
# This is for functions about ui loading
#############################################################################################

#######################################
# imports

import os

from PySide import QtCore, QtGui, QtUiTools

import esa.common.python.lib.logger.logger as logger
import esa.common.python.lib.io.io as io

reload(logger)
reload(io)

#######################################
# functionality


def get_ui_files(folder, recursive=True):
    return io.get_files(folder, extensions=[".ui"], recursive=recursive)


def get_ui_file(name, folder, recursive=True):
    ui_files = get_ui_files(folder, recursive=recursive)

    for ui_file in ui_files:
        if name.replace(".ui", "") == os.path.basename(os.path.splitext(ui_file)[0]):
            return ui_file


def loadUiWidget(uifilename, parent=None):
    """Loads an ui file from a given file.

    Args:
        uifilename (str): Path file of the .ui file to load.
        parent (QWidget, optional): Optional parent for the given ui.

    Returns:
        QWidget: Returns the loaded widget.
    """
    loader = QtUiTools.QUiLoader()

    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)

    oUi = loader.load(uifile, parent)

    uifile.close()

    return oUi


def loadUiWidgetFromPyFile(uifilename, parent=None):
    """Loads the equivalent ui widget from a py file.

    Args:
        uifilename (str): Path file of the .ui file to load.
        parent (QWidget, optional): Optional parent for the given ui.

    Returns:
        QWidget: Returns the loaded widget.
    """
    sUIfile = uifilename.replace(".pyc", ".ui")
    sUIfile = sUIfile.replace(".py", ".ui")
    sUIfile = sUIfile.replace(".exe", ".ui")

    return loadUiWidget(sUIfile, parent=parent)


def get_child(root_element, name):
    """Summary

    Args:
        root_element (QtCore.QObject): UI object root to search recursive the child that has the given name.
        name (str): The name of the ui element that is searched.

    Returns:
        QtCore.QObject: UI object that uses the given name.
    """
    if root_element:
        children = root_element.findChildren(QtCore.QObject, name)
        if children:
            return children[0]

    return None

#######################################
# execution

if __name__ == "__main__":
    # testWindow = loadUiWidget("/usr/people/eduardo-a/dev/toolCage/toolCage/tool/toolManager.ui")
    # testWindow.show()
    # print testWindow
    pass
