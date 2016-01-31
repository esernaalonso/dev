"""Summary"""
#######################################
# imports

import re
import sys
import os
import inspect
import importlib

#######################################
# functionality\


def is_function_in_mod(mod, func):
    """Summary

    Args:
        mod (TYPE): Description
        func (TYPE): Description

    Returns:
        TYPE: Description
    """
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def get_mod_functions(mod):
    """Summary

    Args:
        mod (TYPE): Description

    Returns:
        TYPE: Description
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
            Example: {"name": os, "alias": os, "type": python_module, "path": "C:\\Python27\\lib\\os.py", "source": "import sys, os"}
    """
    # List to store the info dictionaries.
    import_infos = []

    # Gets all import statements from the file
    import_statements = get_file_import_statements(source_file)

    # Loops the statements searching for the info
    for import_statement in import_statements:
        # Each line can have more than one import module, so we need a list.
        mod_names = []

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

        if not matches:
            matches = re.match("from (.*) import (.*)", import_statement)
            if matches:
                from_mods = matches.group(1).split(", ")
                import_mods = matches.group(2).split(", ")

                mod_names = [("%s.%s" % (from_mod, import_mod)) for from_mod in from_mods for import_mod in import_mods]

        if not matches:
            matches = re.match("import (.*) as (.*)", import_statement)

            if matches:
                mod_names = matches.group(1).split(", ")
                import_as = matches.group(2).split(", ")

        if not matches:
            matches = re.match("import (.*)", import_statement)

            if matches:
                mod_names = matches.group(1).split(", ")

        # Loops the independent modules to extract the info from each one.
        for mod_name in mod_names:
            # Loads the module in the memory yo have access to the info.
            mod = importlib.import_module(mod_name)
            if mod:
                # Creates the dictionary to store the module info.
                mod_alias = import_as[0] if import_as else mod_name
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


#######################################
# execution

if __name__ == "__main__":
    testFile = "P:\\dev\\esa\\common\\python\\tool\\template\\templateToolStdUI.py"

    imports = get_file_imports_info(testFile)
    for imp in imports:
        print imp

    pass
