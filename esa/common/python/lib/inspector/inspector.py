"""Summary"""
#######################################
# imports

import re
import sys
import os
import inspect
import importlib

#######################################
# functionality


def is_function_in_mod(mod, func):
    """Checks if a function name is inside a module

    Args:
        mod (imported module): The imported module to search the functions inside.
        func (str): Name of the function to search.

    Returns:
        bool: Returns True if the function is inside the module, False if not.
    """
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def get_mod_functions(mod):
    """Gets all functions that are inside a module.

    Args:
        mod (imported module): The imported module to search the functions inside.

    Returns:
        List of str: Returns a list of all functions names from a module.
    """
    return [func.__name__ for func in mod.__dict__.itervalues() if is_function_in_mod(mod, func)]


def get_file_import_statements(source_file):
    """Gets the import statements lines from a given file. Skips the commented imports.

    Args:
        source_file (string): Path of the file where search the imports in.

    Returns:
        List of strings: List of the import statements lines.
    """
    file_imports = []

    with open(source_file, "r") as f:
        data = f.read()
        f.close()

        regx = re.compile('(.*import .*)', re.MULTILINE)
        matches = regx.findall(data)
        if len(matches) > 0:
            for match in matches:
                match = match.lstrip()
                if not match.startswith("#"):
                    if match.startswith("import") or match.startswith("from"):
                        file_imports.append(match)

    return file_imports


def get_file_imports_info(source_file):
    """Get the file info from each import in the source file.

    Args:
        source_file (string): The file to search the import info from.

    Returns:
        List of dictionaries: List of info dictionaries from the import statements.
            Example: {"name": os, "alias": os, "type": python_module, "path": "C:\Python27\lib\os.py", "source": "import sys, os"}
    """
    # List to store the info dictionaries.
    import_infos = []

    # Gets all import statements from the file
    import_statements = get_file_import_statements(source_file)

    # Loops the statements searching for the info
    for import_statement in import_statements:
        # Each line can have more than one import module, so we need a list.
        mod_names = []
        mod_alias = []

        # Different parts of the string import statement
        from_mods = []
        import_mods = []
        import_as = []

        # Tries to match all possible kind of import statement and get the module names from it.
        matches = None

        if not matches:
            matches = re.match("from (.*) import (.*) as (.*)", import_statement)
            if matches:
                from_mods = matches.group(1).split(", ")
                import_mods = matches.group(2).split(", ")
                import_as = matches.group(3).split(", ")

            mod_names = [("%s.%s" % (from_mod, import_mod)) for from_mod in from_mods for import_mod in import_mods]
            mod_alias = [import_as[0] for from_mod in from_mods for import_mod in import_mods]

        if not matches:
            matches = re.match("from (.*) import (.*)", import_statement)
            if matches:
                from_mods = matches.group(1).split(", ")
                import_mods = matches.group(2).split(", ")

                mod_names = [("%s.%s" % (from_mod, import_mod)) for from_mod in from_mods for import_mod in import_mods]
                mod_alias = [import_mod for from_mod in from_mods for import_mod in import_mods]

        if not matches:
            matches = re.match("import (.*) as (.*)", import_statement)

            if matches:
                mod_names = matches.group(1).split(", ")
                mod_alias = matches.group(2).split(", ")

        if not matches:
            matches = re.match("import (.*)", import_statement)

            if matches:
                mod_names = matches.group(1).split(", ")
                mod_alias = matches.group(1).split(", ")

        # Loops the independent modules to extract the info from each one.
        for mod_name, mod_alias in zip(mod_names, mod_alias):
            # Loads the module in the memory yo have access to the info.
            mod = importlib.import_module(mod_name)
            if mod:
                # Creates the dictionary to store the module info.
                mod_info = {"name": mod_name, "alias": mod_alias, "type": None, "path": None, "source": import_statement}

                # If the module is a builtin_module, it has no path
                if mod_name in sys.builtin_module_names:
                    mod_info["type"] = "builtin_module"
                    mod_info["path"] = None
                else:
                    # If not a builtin_module, can be a python one or a custom one
                    mod_path = inspect.getfile(mod)
                    if os.path.exists(mod_path.replace(".pyc", ".py")):
                        mod_path = mod_path.replace(".pyc", ".py")
                    if os.path.exists(mod_path.replace(".pyo", ".py")):
                        mod_path = mod_path.replace(".pyo", ".py")

                    # Stores the module path
                    mod_info["path"] = mod_path

                    if mod_path.startswith(os.path.dirname(sys.executable)):
                        if "site-packages" in mod_path:
                            mod_info["type"] = "python_package"
                        elif "lib" in mod_path:
                            mod_info["type"] = "python_module"
                    else:
                        mod_info["type"] = "custom_module"

                import_infos.append(mod_info)

    return import_infos


def build_import_statement(import_info, import_style="import", force_relative=False, relative_path=""):
    """Summary

    Args:
        import_info (dictionary): Dictionary with import information.
            Example: {"name": os, "alias": os, "type": python_module, "path": "C:\Python27\lib\os.py", "source": "import sys, os"}
        import_style (str, optional): Indicates if hast to create an "import" statement or a "from * import" one.
            Allowed values: "import", "from"
        force_relative (bool, optional): Indicates if has to assume the import is relative to the current file,
            so no need of full path is needed. Instead of buildind "import lib.subib.subsublib" will do just "import subsublib"

    Returns:
        str: Returns a string with a valid built import statement.
    """
    # Regular import.
    if import_style == "import":
        import_split = import_info["name"].split(".")
        import_name_last_part = import_split[-1:][0]

        # If force relative is indicated, asumes that the import is relative to the current file.
        if force_relative:
            import_info["name"] = ("%s.%s" %(relative_path, import_name_last_part)) if relative_path else import_name_last_part
            import_split = import_info["name"].rsplit('.', 1)
            import_name_last_part = import_split[-1:][0]

        if len(import_split) > 1 or import_name_last_part != import_info["alias"]:
            return ("import %s as %s" % (import_info["name"], import_info["alias"]))
        else:
            return ("import %s" % import_info["name"])
    elif import_style == "from":
        # Splits the name part to see if a from import can be done.
        import_split = import_info["name"].rsplit('.', 1)

        if len(import_split) == 2:
            # If splitted last part is different than the alias, uses the alias
            if import_split[1] != import_info["alias"]:
                return ("from %s import %s as %s" % (import_split[0], import_split[1], import_info["alias"]))
            else:
                # If not, uses the last part and no alias.
                return ("from %s import %s" % (import_split[0], import_info["alias"]))
        else:
            # In this case a from import cannot be done, so a regular one has to be done.
            return build_import_statement(import_info, force_relative=force_relative)
            # return ("import %s as %s" % (import_info["name"], import_info["alias"]))


#######################################
# execution

if __name__ == "__main__":
    testFile = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"

    imports = get_file_imports_info(testFile)
    for imp in imports:
        print build_import_statement(imp)
        print build_import_statement(imp, import_style="from")

    pass
