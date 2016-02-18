python --version 2>NUL

if ERRORLEVEL 1 GOTO NOPYTHON
goto :HASPYTHON

:NOPYTHON
ECHO "INSTALLING PYTHON 2.7"
START /WAIT source/python-2.7.11.amd64.msi
goto :HASPYTHON

:HASPYTHON

ECHO "INSTALLING REQUIRED MODULES"
START /WAIT python -m pip install <module_name>

ECHO "INSTALLING REQUIRED MODULES"
START /WAIT source/vcredist_x64.exe

ECHO "END INSTALL"