"""Summary"""
#######################################
# imports

import os
import shutil
import inspect

import esa.common.python.lib.logger.logger as logger
import esa.common.python.lib.inspector.inspector as inspector
import esa.common.python.lib.io.io as io
import esa.common.python.lib.ui.ui as ui

reload(logger)
reload(inspector)
reload(io)
reload(ui)

#######################################
# functionality

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


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


def setup_file_pack_folder(source_file, remove_previous=False, **kwargs):
    """Creates a pack folder to include all pack files.

    Args:
        source_file (string): The path to the file that will be in the folder to use as pack folder.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.
        **kwargs: Extra arguments to have some more options.
            level (int): Indicates the level of depth in the logs.

    Returns:
        string: The pack folder path if created, None if not.
    """

    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    if source_file:
        pack_folder = os.path.dirname(source_file)

        # if a clean pack is needed, the old one is deleted.
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

            # Finally returns the pack folder created.
            return pack_folder
        else:
            logger.error(("Pack Folder NOT CREATED -> %s" % pack_folder), level=level)
            return None
    else:
        logger.error(("Pack Folder source file must be provided -> %s" % source_file), level=level)
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
            remove_previous (bool): Indicates if removes previous packaging.

    Returns:
        string: The path to the created file. None if not created.
    """

    # Some configurations
    remove_previous_packaging_types = ["main"]
    explorable_packaging_types = ["main", "lib"]
    explorable_file_types = [".py"]
    packable_import_types = ["custom_module"]

    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    packaging_type = "main"
    if "packaging_type" in kwargs: packaging_type = kwargs["packaging_type"]

    remove_previous = False
    if "remove_previous" in kwargs: remove_previous = kwargs["remove_previous"]

    # If source file does not exist, cannot start the packaging.
    if not os.path.exists(source_file):
        logger.error(("File to Pack does not exist -> %s" % source_file), level=level)
        return None

    # Shows info about the file to package.
    logger.info(("Packaging File -> %s" % source_file), level=level)

    # This should be the destination path folder
    # If is the main one, needs to add the subfolder with tool name.
    # If not, the packaging type should be used as subfolder name. If already is in that level, does not add it again.
    package_sub_folder = ""
    if packaging_type == "main":
        package_sub_folder = os.path.basename(os.path.splitext(source_file)[0])
    elif os.path.basename(os.path.normpath(pack_folder)) != packaging_type:
        package_sub_folder = packaging_type
    dest_folder = os.path.join(pack_folder, package_sub_folder)
    logger.info(("Destination Folder -> %s" % dest_folder), level=level)

    # This should be the destination path file
    dest_file = os.path.join(dest_folder, os.path.basename(source_file))
    logger.info(("Destination File -> %s" % dest_file), level=level)

    # If has to remove the previous and it exists, mark it
    remove_previous_folder = remove_previous and packaging_type in remove_previous_packaging_types

    # If dest pack folder does not exist, cannot start the packaging. Tries to create it.
    setup_file_pack_folder(dest_file, remove_previous=remove_previous_folder, level=level+1)

    # Gets the destination file type.
    file_type = os.path.splitext(dest_file)[1]
    logger.info(("File Type -> %s" % dest_file), level=level)

    # Prints the type of packaging.
    logger.info(("Packaging Type -> %s" % packaging_type), level=level)
    shutil.copyfile(source_file, dest_file)

    if os.path.exists(dest_file):
        logger.info(("File Packaged -> %s" % dest_file), level=level)

        # TODO: if the packaging_type is main, need to create the initialization.bat

        # In this case is explorable. Can contain imports, ui dependencies, etc.
        if packaging_type in explorable_packaging_types and file_type in explorable_file_types:
            logger.info(("File can be recursive explored -> %s" % source_file), level=level)

            logger.info(("Searching source file imports -> %s" % source_file), level=level)
            imports_info = inspector.get_file_imports_info(source_file)

            # If it has imports info, packages the imports as libraries
            if imports_info:
                import_relative_path = "lib" if packaging_type=="main" else ""

                for import_info in imports_info:
                    if import_info["type"] in packable_import_types:
                        # Packages the import source as a library
                        logger.info(("Packaging lib file -> %s" % import_info["path"]), level=level)
                        pack_file(import_info["path"], pack_folder=dest_folder, level=level+1, packaging_type="lib")

                        # After packaging the lib, must replace in dest_file the import for the new one.
                        import_statement = inspector.build_import_statement(import_info, force_relative=True, relative_path=import_relative_path)
                        logger.info(("Replacing import -> %s <- with -> %s" % (import_info["source"], import_statement)), level=level)
                        io.replace_line_in_file(dest_file, import_info["source"], import_statement, keep_old_commented=True)

            # Search dependencies like ui files and package them.
            logger.info(("Searching source UI dependencies -> %s" % source_file), level=level)
            ui_search_folder = os.path.dirname(source_file)
            ui_files = inspector.get_file_ui_dependencies(source_file)

            # If it has ui files, packages the imports as libraries
            if ui_files:
                for ui_file in ui_files:
                    # Prints the type of packaging.
                    logger.info(("Packaging UI dependency -> %s" % ui_file), level=level)
                    pack_file(ui_file, pack_folder=dest_folder, level=level+1, packaging_type="ui")

            # Search dependencies like qss files and package them.
            logger.info(("Searching source QSS dependencies -> %s" % source_file), level=level)
            qss_search_folder = os.path.dirname(source_file)
            qss_files = inspector.get_file_qss_dependencies(source_file)

            # If it has qss files, packages the imports as libraries
            if qss_files:
                for qss_file in qss_files:
                    print qss_file
                    # Prints the type of packaging.
                    logger.info(("Packaging QSS dependency -> %s" % qss_file), level=level)
                    pack_file(qss_file, pack_folder=dest_folder, level=level+1, packaging_type=os.path.join("lib", "styles"))

        else:
            logger.info(("Packaging/File Type non explorable. Direct Copy to -> %s" % dest_file), level=level)

        # Finally returns the packaged file path.
        return dest_file
    else:
        logger.error(("File could not be packaged -> %s" % dest_file), level=level)
        return None


# TODO: fill all this past days docstrings and comments

# TODO: fill this function to pack the installer.
# TODO: create the way to see what pip installed packages must be included in the install part.
def pack_installer(source_file, pack_folder=None, **kwargs):
    """Packs a installer folder for the source file and dependencies inside the pack folder, creating a installer folder.

    Args:
        source_file (string): Path to the file to use as root.
        pack_folder (string): The path to the folder to create the intall folder inside.
        **kwargs: Extra arguments like log level, etc.
            remove_previous (bool, optional): Indicates if it has to remove the previous pack intaller folder.
            level (int): Indicates the level of depth in the logs.
    """
    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    remove_previous = False
    if "remove_previous" in kwargs: remove_previous = kwargs["remove_previous"]

    if os.path.exists(source_file):
        install_folder = os.path.join(pack_folder, "install")

        # if a clean pack is needed, the old one is deleted.
        if os.path.exists(install_folder) and remove_previous:
            logger.info(("Removing Current Install Folder -> %s" % install_folder), level=level)
            shutil.rmtree(install_folder)

        # if the install_folder doesn't exist, is created.
        if not os.path.exists(install_folder):
            logger.info(("Creating Install Folder-> %s" % install_folder), level=level)
            os.makedirs(install_folder)

        # If the install_folder is created OK, creates the install content.
        if os.path.exists(install_folder):
            logger.info(("Install Folder Created -> %s" % install_folder), level=level)

            # Pack the sources folder.
            source_folder = os.path.join(get_current_folder(), "install", "source")
            source_dest_folder = os.path.join(install_folder, "source")
            logger.info(("Packaging Instsall Sources Folder -> %s" % source_dest_folder), level=level)
            shutil.copytree(source_folder, source_dest_folder)

            # TODO: pack the install.bat. BETTER IF CREATED ON FLY. Create function for it.

            # TODO: Use the following code to fill the install.bat
            # Searches pip dependent modules to prepare the install.bat for a good resources install.
            pip_dependencies = inspector.get_file_pip_dependencies(source_file, recursive=True)
            print pip_dependencies

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

        # The real pack folder is a new folder with the name of the module in the provided pack folder.
        pack_folder = os.path.join(pack_folder, os.path.basename(os.path.splitext(source_file)[0]))

        # packs the file
        pack_file(source_file, pack_folder=pack_folder, level=1, remove_previous=remove_previous)

        # Creates the installer
        pack_installer(source_file, pack_folder=pack_folder, level=1, remove_previous=remove_previous)
    else:
        logger.error(("Source File must be provided -> %s" % source_file))
        return None

#######################################
# execution

if __name__ == "__main__":
    source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    pack_folder = "F:\\project\\tmp\\pack"

    pack_module(source_file, pack_folder=pack_folder, remove_previous=True)
