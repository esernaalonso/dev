"""Summary"""
#######################################
# imports

import tempfile
import shutil
import os

def replace_line_in_file(source_file, replace_pattern, replace_string, keep_old_commented=False):
    # Creates a temporal file to do the operations
    temp_file_handler, temp_file_path = tempfile.mkstemp(dir=os.path.dirname(source_file))

    # Loops each line
    with open(temp_file_path,'w') as new_file:
        with open(source_file) as old_file:
            for line in old_file:
                # Only if the replace pattern is in the line tries a replace.
                if replace_pattern in line:
                    # If keep old as comment is required, saves current line as a comment.
                    if keep_old_commented:
                        if not line.startswith("#"):
                            new_file.write("#%s" % line)
                        else:
                            new_file.write(line)

                    # Creates the new line with the replacement
                    new_line = line.replace("#", "").replace(replace_pattern, replace_string)
                    new_file.write(new_line)
                else:
                    # If is a regular line, keeps it as it is.
                    new_file.write(line)

    # Closes the temporal file after the operations
    os.close(temp_file_handler)

    # Remove original file and move new file.
    os.remove(source_file)
    shutil.move(temp_file_path, source_file)

#######################################
# functionality


#######################################
# execution

if __name__ == "__main__":
    # test_file = "P:\\tmp\\pack\\templateToolStdUI.py"
    # replace_line_in_file(test_file, "import esa.common.python.lib.utils as utils", "import lib.utils as utils", keep_old_commented=True)

    pass
