#######################################
# imports

import os

import esa.common.python.lib.logger.logger as logger

reload(logger)

#######################################
# functionality


def packPyFile(source_file, pack_folder=None, remove_previous=False, **kwargs):
    logger.info("Searching -> %s" % source_file)
    logger.info("Pack Folder -> %s" % pack_folder)

    if os.path.exists(source_file):
        logger.info(("File Exists -> %s" % source_file), level=1)

#######################################
# execution

if __name__ == "__main__":
    source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    pack_folder = "F:\\project\\tmp\\pack"

    packPyFile(source_file, pack_folder=pack_folder, removePrevious=True)
