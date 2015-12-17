#!/usr/bin/python3
#-*-coding:utf-8-*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
from DatabaseWindow import DatabaseWindow
import globalVar

with DatabaseWindow() as window:
    globalVar.databaseWindow = window
    window.connect("delete_event", Gtk.main_quit)
    Gtk.main()
