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
    """Creates a __init__.py file in the given folder.

    Args:
        source_folder (string): The folder where to create a __init__.py file in.
        **kwargs: Extra arguments to have some more options.
            level (int): Indicates the level of depth in the logs.

    Returns:
        string: Returns the path to the created __init__.py file. None if not created
    """
    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    if source_folder:
        if os.path.exists(source_folder):
            init_file_path = os.path.join(source_folder, "__init__.py")
            if not os.path.exists(init_file_path):
                with open(init_file_path, 'w') as fout:
                    fout.write("")

            if os.path.exists(init_file_path):
                logger.info(("__init__.py file created -> %s" % init_file_path), level=level)
                return init_file_path
            else:
                logger.error(("__init__.py file NOT CREATED -> %s" % init_file_path), level=level)
                return None
        else:
            logger.error(("Source Folder does not exist -> %s" % source_folder), level=level)
            return None
    else:
        logger.error(("Source Folder must be provided -> %s" % source_folder), level=level)
        return None


def setup_pack_folder(pack_folder, remove_previous=False, **kwargs):
    """Creates a pack folder to include all pack files.

    Args:
        pack_folder (string): The path to the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.
        **kwargs: Extra arguments to have some more options.
            level (int): Indicates the level of depth in the logs.

    Returns:
        string: The pack folder path if created, None if not.
    """

    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    if pack_folder:
        # if a clean pack is needed, the old one is deleted.
        if remove_previous:
            if os.path.exists(pack_folder) and remove_previous:
                logger.info(("Removing Current Package Folder -> %s" % pack_folder), level=level)
                shutil.rmtree(pack_folder)

        # if the pack_folder doesn't exist, is created.
        if not os.path.exists(pack_folder):
            logger.info(("Creating Package Folder-> %s" % pack_folder), level=level)
            os.makedirs(pack_folder)

        # If the pack_folder is created OK, creates the lib folder.
        if os.path.exists(pack_folder):
            logger.info(("Package Folder Created -> %s" % pack_folder), level=level)

            # Also creates an __init__ file
            pack_folder_init = create_init_file(pack_folder, level=level+1)
            if not pack_folder_init:
                logger.error(("__init__.py file in Pack Folder NOT CREATED in -> %s" % pack_folder), level=level)
                return None

            # Now creates the lib folder for all dependencies
            pack_folder_lib = os.path.join(pack_folder, "lib")
            logger.info(("Creating Package Lib Folder-> %s" % pack_folder_lib), level=level)
            if not os.path.exists(pack_folder_lib):
                os.makedirs(pack_folder_lib)

            if os.path.exists(pack_folder_lib):
                logger.info(("Package Lib Folder Created -> %s" % pack_folder_lib), level=level)

                # Also creates a __init__ file in the lib folder.
                pack_folder_lib_init = create_init_file(pack_folder_lib, level=level+1)
                if not pack_folder_init:
                    logger.error(("__init__.py file in Pack Lib Folder NOT CREATED in -> %s" % pack_folder_lib), level=level)
                    return None
            else:
                logger.error(("Pack Lib Folder NOT CREATED -> %s" % pack_folder_lib), level=level)
                return None

            # Finally returns the pack folder.
            return pack_folder
        else:
            logger.error(("Pack Folder NOT CREATED -> %s" % pack_folder), level=level)
            return None
    else:
        logger.error(("Pack Folder must be provided -> %s" % pack_folder), level=level)
        return None


def pack_file(source_file, pack_folder=None, recursive=True, **kwargs):
    """Summary

    Args:
        source_file (string): Path of the file to pack.
        pack_folder (string, optional): Destination Pack Folder.
        recursive (bool, optional): Indicates if pack all dependencies. Default True.
        **kwargs: Extra arguments to have some more options.
            level (int): Indicates the level of depth in the logs.
            packaging_type (string): Indicates the type of packaging for the file.

    Returns:
        string: The path to the created file. None if not created.
    """

    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    packaging_type = "main"
    if "packaging_type" in kwargs: packaging_type = kwargs["packaging_type"]

    # If source file does not exist, cannot start the packaging.
    if not os.path.exists(source_file):
        logger.error(("File to Pack does not exist -> %s" % source_file), level=level)
        return None

    # If pack folder does not exist, cannot start the packaging.
    if not os.path.exists(pack_folder):
        logger.error(("Pack Folder does not exist -> %s" % source_file), level=level)
        return None

    # Shows info about the file to package.
    logger.info(("Packaging File -> %s" % source_file), level=level)

    # This should be the destination path
    # TODO: Add here the intermediate folder in case that packaging_type is not main. For example lib
    package_sub_folder = packaging_type if packaging_type != "main" else ""
    dest_file = os.path.join(pack_folder, package_sub_folder, os.path.basename(source_file))
    logger.info(("Destination File -> %s" % dest_file), level=level)

    file_type = os.path.splitext(source_file)[1]
    logger.info(("File Type -> %s" % file_type), level=level)

    # Prints the type of packaging.
    logger.info(("Packaging Type -> %s" % packaging_type), level=level)

    explorable_packaging_types = ["main", "lib"]
    explorable_file_types = [".py"]
    if packaging_type in explorable_packaging_types and file_type in explorable_file_types:
        logger.info(("File can be recursive explored -> %s" % source_file), level=level)
        shutil.copyfile(source_file, dest_file)

        # TODO: In this case is explorable. Must open the destination file and:
        # Search imports and package them recursive in the lib folder.
        # Search dependencies like ui files and package them.
        # Replace in the dest file the imports and dependencies
    else:
        logger.info(("Packaging/File Type non explorable. Direct Copy to -> %s" % dest_file), level=level)
        shutil.copyfile(source_file, dest_file)


def pack_module(source_file, pack_folder=None, remove_previous=True, **kwargs):
    """Packs a python file and all depedencies in and independent module folder.

    Args:
        source_file (string): Path to the file to use as root.
        pack_folder (string): The path to the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.
        **kwargs: Extra arguments like custom dependencies, etc.
    """

    # Initial info.
    logger.info("Searching -> %s" % source_file)
    logger.info("Pack Folder Given -> %s" % pack_folder)

    # If source file exists, can start the packaging.
    if os.path.exists(source_file):
        logger.info(("File Exists -> %s" % source_file))

        # Creates the pack folder if not exists
        # logger.info(("Creating Pack Folder in -> %s" % pack_folder), level=1)
        source_file_name = os.path.basename(os.path.splitext(source_file)[0])
        pack_folder_path = os.path.join(pack_folder, source_file_name)
        pack_folder_path_created = setup_pack_folder(pack_folder_path, remove_previous=remove_previous, logs=True, level=1)
        if not pack_folder_path_created:
            return None

        # If everything was OK, continues the packaging and finally returns the path.
        if os.path.exists(pack_folder_path_created):
            # Calls the packaging process for the main file. This process is recursive, for all import dependencies.
            pack_file(source_file, pack_folder=pack_folder_path_created, level=1)

            # Finally returns the pack folder.
            return pack_folder_path_created
        else:
            logger.error(("Pack Folder could not be created -> %s" % pack_folder_path))
            return None
    else:
        logger.error(("Source File must be provided -> %s" % source_file))
        return None

#######################################
# execution

if __name__ == "__main__":
    source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    pack_folder = "F:\\project\\tmp\\pack"

    pack_module(source_file, pack_folder=pack_folder, removePrevious=True)
