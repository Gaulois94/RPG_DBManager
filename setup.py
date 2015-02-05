#!/usr/bin/python3
#-*-coding:utf-8-*-

from gi.repository import Gtk, GObject, Gdk
from DatabaseWindow import DatabaseWindow
import globalVar

window = DatabaseWindow()
globalVar.databaseWindow = window
window.connect("delete_event", Gtk.main_quit)
Gtk.main()
