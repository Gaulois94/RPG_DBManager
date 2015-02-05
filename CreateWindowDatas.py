from gi.repository import Gtk
from globalVar import *

def windowAdd(databaseWindow, widget):
    window = Gtk.Window(title="Add item")
    window.set_property("modal", True)
