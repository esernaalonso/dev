"""Summary"""
#######################################
# imports

import os
import inspect
import subprocess

import esa.common.python.lib.io.io as io

reload(io)

#######################################
# functionality

def get_current_file():
    return os.path.abspath(inspect.getsourcefile(lambda:0))

def get_current_folder():
    return os.path.dirname(get_current_file())

def get_exe(exe_name):
    valid_exes = ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"]
    exe_name = exe_name + ".exe" if not exe_name.endswith(".exe") else exe_name
    if exe_name in valid_exes:
        candidates = io.get_files(get_current_folder(), extensions=[".exe"], filters=[exe_name])
        if candidates:
            return candidates[0]

def run(command_options, exe_name="ffmpeg.exe"):
    cmd = [get_exe(exe_name), "-hide_banner"] + command_options
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = process.communicate()
        return out
    except Exception as e:
        return str(e)

#######################################
# execution

if __name__ == "__main__":
    url = "http://www.db.insideanim.com/media/campus/tmp/creatures01_lsn01_sbt01_the_basis_of_animal_behavior.flv"
    ffmpeg_options = ["-i", url]
    output = run(ffmpeg_options, exe_name="ffprobe.exe")
    print "-----------------------------------"
    print output
    print "-----------------------------------"
    pass
