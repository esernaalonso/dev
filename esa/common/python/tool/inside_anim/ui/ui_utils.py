"""Summary"""

#######################################
# imports

import os
import inspect

#######################################
# functionality

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))

def get_folder():
    return os.path.dirname(get_current_file())

#######################################
# execution

if __name__ == "__main__":
    pass
