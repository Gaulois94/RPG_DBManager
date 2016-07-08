from gi.repository import Gtk

direction = Gtk.ListStore(str)
direction.append("TOP")
direction.append("BOTTOM")
direction.append("RIGHT")
direction.append("LEFT")
