from gi.repository import Gtk
from globalVar import *
from functions import *
from TreeTab import TreeTab
from globalVar import *

animTypeModel = Gtk.ListStore(str)
animTypeModel.append(["Static"])
animTypeModel.append(["Dynamic"])

unitStore = Gtk.ListStore(str)
