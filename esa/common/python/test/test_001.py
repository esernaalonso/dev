import pysideuic as pui

file_ui = "P:/dev/esa/common/python/lib/streaming/ui/streaming.ui"
file_py = "P:/dev/esa/common/python/lib/streaming/ui/streaming_ui_generated.py"
file_py_f = open(file_py, "w")
pui.compileUi(file_ui, file_py_f)
file_py_f.close()
