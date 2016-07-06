from gi.repository import Gtk
from globalVar import *
from functions import *
from TreeTab import TreeTab
import databaseFunctions

class AnimationTab(TreeTab):
    def __init__(self, window):
        self.databaseWindow = window
        store = Gtk.TreeStore(*[x[1] for x in animModel])
        TreeTab.__init__(self, store)

        for i, value in enumerate(animModel):
            renderer = None

            if value[0] == "Unit Name":
                renderer = Gtk.CellRendererText()
                renderer.set_property("editable", False);

            else if value[0] == "Type":
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("model", AnimTypeModel.animTypeModel)
                renderer.set_property("text-column", 0)
                renderer.set_property("editable", True)
                renderer.connect("edited", self.editType)

            else:
                renderer = Gtk.CellRendererText()
                renderer.set_property("editable", True)

            column = Gtk.TreeViewColumn(value[0], renderer, text=i)
            column.set_resizable(True)
            column.set_expand(True)
            self.tree.append_column(column)

    def createHandleManager(self):
        grid = Gtk.Grid(orientation = Gtk.Orientation.VERTICAL)
        grid.set_halign(Gtk.Align.END)
        grid.set_valign(Gtk.Align.END)

        unitLabel = Gtk.Label("Unit Name")
        nameLabel = Gtk.Label("Animation Name")
        typeLabel = Gtk.Label("Type")

        self.unitWidget = Gtk.ComboBox.new_with_model(self.databaseWindow.unitTab.store)
        cell            = Gtk.CellRendererText()
        self.unitWidget.pack_start(cell, True)
        self.unitWidget.add_attribute(cell, "text", 2)

        self.nameWidget = Gtk.Entry()

        self.typeWidget = Gtk.ComboBox.new_with_model(AnimTypeModel.animTypeModel)
        cell            = Gtk.CellRendererText()
        self.typeWidget.pack_start(cell, True)
        self.typeWidget.add_attribute(cell, "text", 0)

        valueGrid = Gtk.Grid(orientation = Gtk.Orientation.VERTICAL)
        valueGrid.attach(unitLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.unitWidget, unitLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(nameLabel, unitLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(typeLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.typeWidget, typeLabel, Gtk.PositionType.RIGHT, 3, 1)

        buttonBox = Gtk.Box()
        okButton  = Gtk.Button(label="Add")
        okButton.connect("clicked", self.addEntry)

        buttonBox.add(okButton)
        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        grid.add(valueGrid)
        grid.add(buttonBox)

        return grid

    def addEntry(self, widget):
        pass

    def editType(self):
        pass
