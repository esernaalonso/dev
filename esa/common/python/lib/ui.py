"""Summary"""
############################################################################################
# This is for functions about ui loading
#############################################################################################

#######################################
# imports

from PySide import QtCore, QtGui, QtUiTools

#######################################
# functionality


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
