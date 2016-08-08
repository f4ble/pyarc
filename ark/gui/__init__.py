from factory import Factory
import ark
from tkinter import Tk
from ark.gui.gui_class import PyArcGui

def init():
    root = Tk()

    root.title(PyArcGui.gui_title)
    root.geometry(PyArcGui.gui_size)

    app = PyArcGui(root)
    Factory.set('GUI',app)

    from ark.gui.control import Control
    Factory.set('GUI_CONTROL',Control)

    ark.init()
    print('RUNNING GUI')

    root.mainloop()
