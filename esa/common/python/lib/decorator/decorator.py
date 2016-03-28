"""Summary"""
#######################################
# imports

from PySide import QtCore, QtGui

import esa.common.python.lib.logger.logger as logger

#######################################
# functionality

def wait_cursor(function):
    def new_function(*args, **kwargs):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            function(*args, **kwargs)
        except Exception as e:
            logger.warning(("Wait Cursor Setup Error -> %s" % str(e)), level=0)
            raise e
        finally:
            QtGui.QApplication.restoreOverrideCursor()
    return new_function

#######################################
# execution

if __name__ == "__main__":
    pass
