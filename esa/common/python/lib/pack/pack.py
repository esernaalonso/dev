"""Summary"""
#######################################
# imports

import os
import shutil
import inspect
import compileall

import esa.common.python.lib.logger.logger as logger
import esa.common.python.lib.inspector.inspector as inspector
import esa.common.python.dist.dist as dist
import esa.common.python.lib.io.io as io
import esa.common.python.lib.ui.ui as ui

# reload(logger)
# reload(inspector)
# reload(io)
# reload(ui)

#######################################
# functionality

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def create_install_bat(install_bat_file, remove_previous=False, **kwargs):
    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    # if a clean is needed, the old one is deleted.
    if os.path.exists(install_bat_file) and remove_previous:
        logger.info(("Removing Current install.bat -> %s" % install_bat_file), level=level)
        os.remove(install_bat_file)

    # if the install_bat_file doesn't exist, is created.
    if not os.path.exists(install_bat_file):
        logger.info(("Creating install.bat -> %s" % install_bat_file), level=level)
        install_bat_source_file = os.path.join(get_current_folder(), "install", "install.bat")
        shutil.copyfile(install_bat_source_file, install_bat_file)

        # Searches pip dependent modules to prepare the install.bat for a good resources install.
        if os.path.exists(install_bat_file):
            pip_dependencies = inspector.get_file_pip_dependencies(source_file, recursive=True)
            if pip_dependencies:
                for pip_dependency in pip_dependencies:
                    logger.info(("Setting up pip module install -> %s" % pip_dependency), level=level)
                    pip_pattern = "REM START /WAIT python -m pip install <module_name>"
                    pip_string = "START /WAIT python -m pip install <module_name>"
                    pip_string = pip_pattern + "\n" + pip_string.replace("<module_name>", pip_dependency)
                    io.replace_line_in_file(install_bat_file, pip_pattern, pip_string)


def create_execute_bat(execute_bat_file, execution_file_name, remove_previous=False, compiled=True, standalone=True, **kwargs):
    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    # if a clean is needed, the old one is deleted.
    if os.path.exists(execute_bat_file) and remove_previous:
        logger.info(("Removing Current execute.bat -> %s" % execute_bat_file), level=level)
        os.remove(execute_bat_file)

    # if the execute_bat_file doesn't exist, is created.
    if not os.path.exists(execute_bat_file):
        logger.info(("Creating execute.bat -> %s" % execute_bat_file), level=level)
        execute_bat_source_file = os.path.join(get_current_folder(), "source", "execute.bat")
        shutil.copyfile(execute_bat_source_file, execute_bat_file)

        # Searches pip dependent modules to prepare the install.bat for a good resources install.
        if os.path.exists(execute_bat_file):
            logger.info(("Setting up execution string -> %s" % execute_bat_file), level=level)
            execute_pattern = "START <python_command> <file_name>"
            execute_string = "START <python_command> <file_name>"

            if standalone:
                execute_string = execute_string.replace("<python_command>", os.path.join("python_dist", "python.exe"))
            else:
                execute_string = execute_string.replace("<python_command>", "python")

            if compiled:
                execution_file_name = execution_file_name.replace(".py", ".pyc")

            execute_string = execute_string.replace("<file_name>", execution_file_name)
            io.replace_line_in_file(execute_bat_file, execute_pattern, execute_string)


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
            packaging_mode (string): Indicates the packaging mode for the file. To do special operations.
            packaging_type (string): Indicates the type of packaging for the file.
            remove_previous (bool): Indicates if removes previous packaging.

    Returns:
        string: The path to the created file. None if not created.
    """

    # Some configurations
    remove_previous_packaging_modes = ["root"]
    explorable_packaging_types = ["lib"]
    explorable_file_types = [".py"]
    packable_import_types = ["custom_module"]

    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    packaging_mode = "root"
    if "packaging_mode" in kwargs: packaging_mode = kwargs["packaging_mode"]

    packaging_type = "lib"
    if "packaging_type" in kwargs: packaging_type = kwargs["packaging_type"]

    remove_previous = False
    if "remove_previous" in kwargs: remove_previous = kwargs["remove_previous"]

    compiled = True
    if "compiled" in kwargs: compiled = kwargs["compiled"]

    standalone = True
    if "standalone" in kwargs: standalone = kwargs["standalone"]

    # If source file does not exist, cannot start the packaging.
    if not os.path.exists(source_file):
        logger.error(("File to Pack does not exist -> %s" % source_file), level=level)
        return None

    # Shows info about the file to package.
    logger.info(("Packaging File -> %s" % source_file), level=level)

    # This should be the destination path folder
    # If is the root one, needs to add the subfolder with tool name.
    # If not, the packaging type should be used as subfolder name. If already is in that level, does not add it again.
    package_sub_folder = ""
    if packaging_mode == "root":
        # package_sub_folder = os.path.basename(os.path.splitext(source_file)[0])
        package_sub_folder = ""
    elif os.path.basename(os.path.normpath(pack_folder)) != packaging_type:
        package_sub_folder = packaging_type
        if not package_sub_folder.startswith("lib") and os.path.basename(os.path.normpath(pack_folder)) != "lib":
            package_sub_folder = os.path.join("lib", package_sub_folder)
    dest_folder = os.path.join(pack_folder, package_sub_folder)
    logger.info(("Destination Folder -> %s" % dest_folder), level=level)

    # This should be the destination path file
    dest_file = os.path.join(dest_folder, os.path.basename(source_file))
    logger.info(("Destination File -> %s" % dest_file), level=level)

    # If has to remove the previous and it exists, mark it
    remove_previous_folder = remove_previous and packaging_mode in remove_previous_packaging_modes

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

        # If the packaging_mode is root, need to create the execute.bat
        if packaging_mode == "root":
            execute_bat_file = os.path.join(os.path.dirname(dest_file), "execute.bat")
            create_execute_bat(execute_bat_file, os.path.basename(dest_file), compiled=compiled, standalone=standalone, remove_previous=True, level=level+1)

        # In this case is explorable. Can contain imports, ui dependencies, etc.
        if packaging_type in explorable_packaging_types and file_type in explorable_file_types:
            logger.info(("File can be recursive explored -> %s" % source_file), level=level)

            logger.info(("Searching source file imports -> %s" % source_file), level=level)
            imports_info = inspector.get_file_imports_info(source_file)

            # If it has imports info, packages the imports as libraries
            if imports_info:
                import_relative_path = "lib" if packaging_mode == "root" else ""

                for import_info in imports_info:
                    if import_info["type"] in packable_import_types:
                        # Packages the import source as a library
                        logger.info(("Packaging lib file -> %s" % import_info["path"]), level=level)
                        pack_file(import_info["path"], pack_folder=dest_folder, level=level+1, packaging_type="lib", packaging_mode="regular")

                        # After packaging the lib, must replace in dest_file the import for the new one.
                        import_statement = inspector.build_import_statement(import_info, force_relative=True, relative_path=import_relative_path)
                        logger.info(("Replacing import -> %s <- with -> %s" % (import_info["source"], import_statement)), level=level)
                        io.replace_line_in_file(dest_file, import_info["source"], import_statement, keep_old_commented=True)

            # Search dependencies like ui files and package them.
            logger.info(("Searching source UI dependencies -> %s" % source_file), level=level)
            ui_search_folder = os.path.dirname(source_file)
            ui_files = inspector.get_file_ui_dependencies(source_file)

            # If it has ui files, packages the files as uis
            if ui_files:
                for ui_file in ui_files:
                    # Prints the type of packaging.
                    logger.info(("Packaging UI dependency -> %s" % ui_file), level=level)
                    pack_file(ui_file, pack_folder=dest_folder, level=level+1, packaging_type="uis", packaging_mode="regular")

            # Search dependencies like png and jpg files and package them.
            logger.info(("Searching source Image dependencies -> %s" % source_file), level=level)
            image_search_folder = os.path.dirname(source_file)
            image_files = inspector.get_file_image_dependencies(source_file)

            # If it has image files, packages the files as images
            if image_files:
                for image_file in image_files:
                    # Prints the type of packaging.
                    logger.info(("Packaging Image dependency -> %s" % image_file), level=level)
                    pack_file(image_file, pack_folder=dest_folder, level=level+1, packaging_type="images", packaging_mode="regular")

            # Search dependencies like qss files and package them.
            logger.info(("Searching source QSS dependencies -> %s" % source_file), level=level)
            qss_search_folder = os.path.dirname(source_file)
            qss_files = inspector.get_file_qss_dependencies(source_file)

            # If it has qss files, packages the files as themes
            if qss_files:
                for qss_file in qss_files:
                    # Prints the qss dependency.
                    logger.info(("Packaging QSS dependency -> %s" % qss_file), level=level)
                    # pack_file(qss_file, pack_folder=dest_folder, level=level+1, packaging_type=os.path.join("lib", "styles"), packaging_mode="regular")
                    pack_file(qss_file, pack_folder=dest_folder, level=level+1, packaging_type="styles", packaging_mode="regular")

            # Search dependencies like font .ttf files and package them.
            logger.info(("Searching source font TTF dependencies -> %s" % source_file), level=level)
            font_search_folder = os.path.dirname(source_file)
            font_files = inspector.get_file_font_dependencies(source_file)

            # If it has ttf files, packages the files as fonts
            if font_files:
                for font_file in font_files:
                    # Prints the font dependency.
                    logger.info(("Packaging TTF dependency -> %s" % font_file), level=level)
                    # pack_file(font_file, pack_folder=dest_folder, level=level+1, packaging_type=os.path.join("lib", "fonts"), packaging_mode="regular")
                    pack_file(font_file, pack_folder=dest_folder, level=level+1, packaging_type="fonts", packaging_mode="regular")

            # Search dependencies like qss files and package them.
            logger.info(("Searching source EXE dependencies -> %s" % source_file), level=level)
            exe_search_folder = os.path.dirname(source_file)
            exe_files = inspector.get_file_exe_dependencies(source_file)

            # If it has exe files, packages the files as exes
            if exe_files:
                for exe_file in exe_files:
                    # Prints the exe dependency.
                    logger.info(("Packaging EXE dependency -> %s" % exe_file), level=level)
                    # pack_file(exe_file, pack_folder=dest_folder, level=level+1, packaging_type=os.path.join("lib", "exes"), packaging_mode="regular")
                    pack_file(exe_file, pack_folder=dest_folder, level=level+1, packaging_type="exes", packaging_mode="regular")

        else:
            logger.info(("Packaging/File Type non explorable. Direct Copy to -> %s" % dest_file), level=level)

        # Finally returns the packaged file path.
        return dest_file
    else:
        logger.error(("File could not be packaged -> %s" % dest_file), level=level)
        return None


def pack_installer(source_file, pack_folder=None, **kwargs):
    """Packs a installer folder for the source file and dependencies inside the pack folder, creating a installer folder.

    Args:
        source_file (string): Path to the file to use as root.
        pack_folder (string): The path to the folder to create the intall folder inside.
        **kwargs: Extra arguments like log level, etc.
            remove_previous (bool, optional): Indicates if it has to remove the previous pack installer folder.
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
            logger.info(("Packaging Install Sources Folder -> %s" % source_dest_folder), level=level)
            shutil.copytree(source_folder, source_dest_folder)

            # Creates the install.bat with all the steps.
            install_bat_file = os.path.join(install_folder, "install.bat")
            create_install_bat(install_bat_file, remove_previous=True, level=level+1)


def pack_dist(pack_folder=None, **kwargs):
    """Packs a installer folder for the source file and dependencies inside the pack folder, creating a installer folder.

    Args:
        pack_folder (string): The path to the folder to create the python dist folder inside.
        **kwargs: Extra arguments like log level, etc.
            remove_previous (bool, optional): Indicates if it has to remove the previous pack dist folder.
            level (int): Indicates the level of depth in the logs.
    """
    # Gets the logs level values from the kwargs
    level = 0
    if "level" in kwargs: level = kwargs["level"]

    remove_previous = False
    if "remove_previous" in kwargs: remove_previous = kwargs["remove_previous"]

    if os.path.exists(source_file):
        dist_folder = os.path.join(pack_folder, "python_dist")

        # if a clean pack is needed, the old one is deleted.
        if os.path.exists(dist_folder) and remove_previous:
            logger.info(("Removing Current Dist Folder -> %s" % dist_folder), level=level)
            shutil.rmtree(dist_folder)

        # if the dist_folder doesn't exist, is created.
        if not os.path.exists(dist_folder):
            logger.info(("Creating Dist Folder -> %s" % dist_folder), level=level)

            # Pack the dist folder.
            source_dist_folder = dist.get_dist_folder(type="miniconda2")
            if source_dist_folder and os.path.exists(source_dist_folder):
                logger.info(("Packaging Dist Folder -> %s" % source_dist_folder), level=level)
                shutil.copytree(source_dist_folder, dist_folder)

                # Once is created, removes some unnecesary folders.
                if os.path.exists(dist_folder):
                    logger.info(("Dist Folder Packaged -> %s" % dist_folder), level=level)
                    logger.info(("Removing Unused Folders and Files from Dist Folder -> %s" % dist_folder), level=level)
                    shutil.rmtree(os.path.join(dist_folder, "conda-meta"))
                    shutil.rmtree(os.path.join(dist_folder, "envs"))
                    shutil.rmtree(os.path.join(dist_folder, "info"))
                    shutil.rmtree(os.path.join(dist_folder, "pkgs"))
                    os.remove(os.path.join(dist_folder, "Uninstall-Anaconda.exe"))


def pack_module(source_file, pack_folder=None, custom_name=None, remove_previous=True, compiled=True, standalone=True, **kwargs):
    """Packs a python file and all depedencies in and independent module folder.

    Args:
        source_file (string): Path to the file to use as root.
        pack_folder (string): The path to the folder to use as pack folder.
        custom_name (string, optional): Custom name for the packed module folder structure.
        remove_previous (bool, optional): Indicates if it has to remove the previous pack folder.
        compiled (bool, optional): Indicates if it has to compile the .py files into .pyc.
        standalone (bool, optional): Indicates if it has to be executable standalone or needs python installed.
        **kwargs: Extra arguments like custom dependencies, etc.
    """

    # Initial info.
    logger.info("Searching -> %s" % source_file)
    logger.info("Pack Folder Given -> %s" % pack_folder)

    # If source file exists, can start the packaging.
    if os.path.exists(source_file):
        logger.info(("File Exists -> %s" % source_file))

        # This will be the module name. Uses the given file name as module name if a custom name is not provided
        module_name = os.path.basename(os.path.splitext(source_file)[0]) if not custom_name else custom_name

        # pack_installer_folder = os.path.join(pack_folder, module_name)
        pack_module_folder = os.path.join(pack_folder, module_name)

        # Creates the installer
        # The real pack folder is a new folder with the name of the module in the provided pack folder.
        # pack_installer(source_file, pack_folder=pack_installer_folder, level=1, remove_previous=remove_previous)

        # Packs the file. Creates one more level folder to contain the actual application.
        # pack_module_folder = os.path.join(pack_folder, module_name, module_name)
        # pack_module_folder = os.path.join(pack_folder, module_name)
        pack_file(source_file, pack_folder=pack_module_folder, level=1, remove_previous=remove_previous, standalone=standalone, compiled=compiled)

        # Compiles the .py into .pyc and deletes the .py files if requested.
        if compiled:
            compileall.compile_dir(pack_module_folder, force=True)
            py_files = io.get_files(pack_module_folder, extensions=[".py"])
            for py_file in py_files:
                os.remove(py_file)

        # Creates the python dist in case the mode is standalone:
        if standalone:
            pack_dist(pack_folder=pack_module_folder, level=1, remove_previous=remove_previous)

        logger.info("Packaging Finished -> %s" % source_file)

    else:
        logger.error(("Source File must be provided -> %s" % source_file))
        return None

#######################################
# execution

if __name__ == "__main__":
    # source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI_launcher.py"
    # source_file = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"
    # source_file = "P:\\dev\\esa\\common\\python\\tool\\inside_anim\\campus\\inside_anim_campus_launcher.py"
    source_file = "P:\\dev\\esa\\common\\python\\tool\\inside_anim\\campus\\inside_anim_campus.py"
    # source_file = "P:\\dev\\esa\\common\\python\\tool\\inside_anim\\campus\\summus_monitor_test_launcher.py"
    # source_file = "P:\\dev\\esa\\common\\python\\tool\\esa_player\\esa_player_launcher.py"

    pack_folder = "F:\\project\\tmp\\pack"

    pack_module(source_file, pack_folder=pack_folder, custom_name="inside_anim_campus", remove_previous=True)
    # pack_module(source_file, pack_folder=pack_folder, custom_name="summus_monitor_test", remove_previous=True)
    # pack_module(source_file, pack_folder=pack_folder, custom_name="esa_player", remove_previous=True)
    # pack_module(source_file, pack_folder=pack_folder, custom_name="template_tool", remove_previous=True)
