"""Summary"""
#######################################
# imports

import os
import shutil

import esa.common.python.lib.logger.logger as logger

reload(logger)

#######################################
# functionality


def create_init_file(source_folder, **kwargs):
    if source_folder:
        # Gets the logs and level values from the kwargs
        logs = False
        level = 0

        if "logs" in kwargs:
            logs = kwargs["logs"]
        if "level" in kwargs:
            level = kwargs["level"]

        if os.path.exists(source_folder):
            init_file_path = os.path.join(source_folder, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, 'w') as fout:
                    fout.write("")

        if os.path.exists(init_file_path):
            return init_file_path


def setup_pack_folder(pack_folder, remove_previous=False, **kwargs):
    """Creates a pack folder to include all pack files.

    Args:
        pack_folder (string): The path to the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.

    Returns:
        string: The file path if created, None if not.
    """

    if pack_folder:
        # Gets the logs and level values from the kwargs
        logs = False
        level = 0

        if "logs" in kwargs:
            logs = kwargs["logs"]
        if "level" in kwargs:
            level = kwargs["level"]

        # if a clean pack is needed, the old one is deleted.
        if remove_previous:
            if os.path.exists(packFolder) and removePrevious:
                if logs:
                    logger.info(("Removing Current Package Folder -> %s" % pack_folder), level=level)
                shutil.rmtree(packFolder)

        # if the pack_folder doesn't exist, is created.
        if not os.path.exists(pack_folder):
            if logs:
                logger.info(("Creating Package Folder-> %s" % pack_folder), level=level)
            os.makedirs(pack_folder)

        # If the pack_folder is created OK, creates the lib folder.
        if os.path.exists(pack_folder):
            if logs:
                logger.info(("Package Folder Created -> %s" % pack_folder), level=level)

            # Also creates an __init__ file
            pack_folder_init = create_init_file(pack_folder, **kwargs)
            if not pack_folder_init:
                if logs:
                    logger.error(("__init__.py file in Pack Folder NOT CREATED in -> %s" % pack_folder), level=level)
                return None

            # Now creates the lib folder for all dependencies
            pack_folder_lib = os.path.join(pack_folder, "lib")
            if logs:
                logger.info(("Creating Package Lib Folder-> %s" % pack_folder_lib), level=level)
            if not os.path.exists(pack_folder_lib):
                os.makedirs(pack_folder_lib)

            if os.path.exists(pack_folder_lib):
                if logs:
                    logger.info(("Package Lib Folder Created -> %s" % pack_folder_lib), level=level)

                # Also creates a __init__ file in the lib folder.
                pack_folder_lib_init = create_init_file(pack_folder_lib)
                if not pack_folder_init:
                    if logs:
                        logger.error(("__init__.py file in Pack Lib Folder NOT CREATED in -> %s" % pack_folder_lib), level=level)
                    return None
            else:
                if logs:
                    logger.error(("Pack Lib Folder NOT CREATED -> %s" % pack_folder_lib), level=level)
                return None

            return pack_folder
        else:
            if logs:
                logger.error(("Pack Folder NOT CREATED -> %s" % pack_folder), level=level)
            return None


def pack_module(source_file, pack_folder=None, remove_previous=False, **kwargs):
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
        # logger.info(("Creating Pack Folder in -> %s" % pack_folder), level=1)
        source_file_name = os.path.basename(os.path.splitext(source_file)[0])
        pack_folder_path = os.path.join(pack_folder, source_file_name)
        pack_folder_path_created = setup_pack_folder(pack_folder_path, remove_previous=remove_previous, logs=True, level=1)
        if not pack_folder_path_created:
            return None

        # TODO: Continue working in the packaging

        # If everything was OK, returns the path.
        if os.path.exists(pack_folder_path_created):
            return pack_folder_path_created
        else:
            logger.error(("Pack Folder could not be created -> %s" % pack_folder_path), level=1)
            return None
    else:
        logger.error(("Source File must be provided -> %s" % source_file), level=1)
        return None

#######################################
# execution

if __name__ == "__main__":
    source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    pack_folder = "F:\\project\\tmp\\pack"

    pack_module(source_file, pack_folder=pack_folder, removePrevious=True)
