"""Summary"""
#######################################
# imports

import os
import shutil

import esa.common.python.lib.logger.logger as logger

reload(logger)

#######################################
# functionality


def create_init_file(source_folder):
    if source_folder:
        if os.path.exists(source_folder):
            init_file_path = os.path.join(source_folder, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, 'w') as fout:
                    fout.write("")

        if os.path.exists(init_file_path):
            return init_file_path


def setup_pack_folder(pack_folder, remove_previous=False):
    """Creates a pack folder to include all pack files.

    Args:
        pack_folder (string): The path to the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.

    Returns:
        string: The file path if created, None if not.
    """

    if pack_folder:
        # if a clean pack is needed, the old one is deleted
        if remove_previous:
            if os.path.exists(packFolder) and removePrevious:
                shutil.rmtree(packFolder)

        # if the packFolder doesn't exist, is created
        if not os.path.exists(pack_folder):
            os.makedirs(pack_folder)

        if os.path.exists(pack_folder):
            return pack_folder


def pack_to_module(source_file, pack_folder=None, remove_previous=False, **kwargs):
    """Packs a python file and all depedencies in and independent module folder.

    Args:
        source_file (string): Path to the file to use as root.
        pack_folder (string): The path to the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.
        **kwargs: Extra arguments like custom dependencies, etc.
    """

    # Initial info.
    logger.info("Searching -> %s" % source_file)
    logger.info("Pack Folder -> %s" % pack_folder)

    # If source file exists, can start the packaging.
    if os.path.exists(source_file):
        logger.info(("File Exists -> %s" % source_file), level=1)

        # Creates the pack folder if not exists
        logger.info(("Creating Pack Folder in -> %s" % pack_folder), level=1)
        source_file_name = os.path.basename(os.path.splitext(source_file)[0])
        pack_folder_path = os.path.join(pack_folder, source_file_name)
        pack_folder_path_created = setup_pack_folder(pack_folder_path, remove_previous=remove_previous)
        if pack_folder_path_created:
            logger.info(("Pack Folder Created -> %s" % pack_folder_path_created), level=1)
        else:
            logger.error(("Pack Folder NOT CREATED -> %s" % pack_folder_path), level=1)
            return None

        # Creates the __init__ file in the pack folder
        logger.info(("Creating __init__.py file in Pack Folder -> %s" % pack_folder), level=1)
        init_file_path = create_init_file(pack_folder_path)
        if init_file_path:
            logger.info(("Created __init__.py file in Pack Folder -> %s" % init_file_path), level=1)
        else:
            logger.error(("__init__.py file in Pack Folder NOT CREATED -> %s" % init_file_path), level=1)
            return None

        # If everything was OK, returns True.
        if os.path.exists(pack_folder_path):
            return pack_folder_path

#######################################
# execution

if __name__ == "__main__":
    source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    pack_folder = "F:\\project\\tmp\\pack"

    pack_to_module(source_file, pack_folder=pack_folder, removePrevious=True)
