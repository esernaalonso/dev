"""Summary"""
#######################################
# imports

import contextlib

from PySide import QtCore, QtGui

import esa.common.python.lib.logger.logger as logger

#######################################
# functionality

@contextlib.contextmanager
def wait_cursor():
    try:
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        yield
    except Exception as e:
        logger.warning(("Wait Cursor Setup Error -> %s" % str(e)), level=0)
        raise e
    finally:
        QtGui.QApplication.restoreOverrideCursor()

#######################################
# execution

if __name__ == "__main__":
    pass
