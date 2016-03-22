"""Summary"""
#######################################
# imports

import inspect
import os

#######################################
# functionality


def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))


def get_current_folder():
    return os.path.dirname(get_current_file())


def get_dist_folder(type="miniconda2"):
    dist_folder = os.path.join(get_current_folder(), type)
    if os.path.exists(dist_folder):
        return dist_folder


#######################################
# execution

if __name__ == "__main__":
    pass
