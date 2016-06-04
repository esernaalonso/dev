import subprocess
import shlex
import os

working_dir = os.path.dirname(os.path.realpath(__file__))

commands = []

commands.append('npm run package')

for cmd in commands:
    cmd_split = shlex.split(cmd)
    proc = subprocess.Popen(cmd_split, cwd=working_dir, shell=True)
    proc.communicate()
    proc.wait()
