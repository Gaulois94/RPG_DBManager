from gi.repository import Gtk
from Tab import Tab
from globalVar import *

class ItemTab(Tab):
    def __init__(self, windowDatabase):
        self.windowDatabase = windowDatabase
        store = Gtk.ListStore(int, str, str)
        Tab.__init__(self, store)

        for i, value in enumerate(itemModel):
            renderer = Gtk.CellRendererText()
            if value != "ID":
                renderer.set_property("editable", True)
            renderer.connect("edited", self.editRenderer, value)
            column   = Gtk.TreeViewColumn(value, renderer, text=i)
            column.set_resizable(True)
            column.set_expand(True)
            self.tree.append_column(column)

        self.itemCapacities = list()

    def createHandleManager(self):
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        grid.set_halign(Gtk.Align.END)
        grid.set_valign(Gtk.Align.END)

        nameLabel = Gtk.Label("Name")
        descriptionLabel = Gtk.Label("Description")

        self.nameWidget = Gtk.Entry()
        scrollDescriptionWidget = Gtk.ScrolledWindow()
        self.descriptionWidget  = Gtk.TextView()
        self.descriptionWidget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrollDescriptionWidget.add(self.descriptionWidget)
        scrollDescriptionWidget.set_size_request(50, 100)

        valueGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        valueGrid.attach(nameLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT, 3, 1)
        valueGrid.attach_next_to(descriptionLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(scrollDescriptionWidget, descriptionLabel, Gtk.PositionType.RIGHT, 3, 1)

        buttonBox = Gtk.Box()

        reinitButton  = Gtk.Button(label="Reinit")
        reinitButton.connect("clicked", self.resetEntries)

        okButton  = Gtk.Button(label="Add")
        okButton.connect("clicked", self.addEntry)

        buttonBox.add(reinitButton)
        buttonBox.add(okButton)

        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        grid.add(valueGrid)
        grid.add(buttonBox)

        return grid

    def addEntry(self, widget):
        return
    
    def resetEntries(self, widget):
        return

    def editRenderer(self, renderer):
        return
