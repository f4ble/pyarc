from configs.config_base import ConfigBase
ConfigBase.load_config()

from translation import Translation
from factory import Factory

trans = Translation()
Factory.set('Translation',trans)

import ark
from tkinter import Tk
from ark.gui import PyArcGui

root = Tk()

root.title(PyArcGui.gui_title)
root.geometry(PyArcGui.gui_size)

app = PyArcGui(root)
Factory.set('GUI',app)
ark.init()
print('RUNNING GUI')

root.mainloop()
