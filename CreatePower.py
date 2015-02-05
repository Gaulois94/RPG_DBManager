from gi.repository import Gtk
from EditPower import EditPower
from copy import copy
from functions import *

class CreatePower:
    def __init__(self, editPower):
        self.editPower = editPower
        self.power = Power()
        self.store = Gtk.ListStore(str, str)

        self.window = None

        typeRenderer = Gtk.CellRendererCombo()
        typeRenderer.set_property("model", self.editPower.store)
        typeRenderer.set_property("text-column", 0)
        typeRenderer.set_property("editable", True)
        typeRenderer.connect("edited", self.editRenderer, "Type")

        typeColumn = Gtk.TreeViewColumn("Power", typeRenderer, text=0);
        typeColumn.set_resizable(True)
        typeColumn.set_expand(True)

        valueRenderer = Gtk.CellRendererText()
        valueRenderer.set_property("editable", True)
        valueRenderer.connect("edited", self.editRenderer, "Value")
        valueColumn = Gtk.TreeViewColumn("Value", valueRenderer, text=1);
        valueColumn.set_resizable(True)
        valueColumn.set_expand(True)

        self.tree = Gtk.TreeView(model = self.store)
        self.tree.append_column(typeColumn)
        self.tree.append_column(valueColumn)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        menuBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        typeLabel = Gtk.Label("Type")
        self.valueLabel = Gtk.Label("Value")

        self.typeWidget = Gtk.ComboBoxText.new()
        self.typeWidget.set_model(editPower.store)

        self.valueWidget = Gtk.Entry()

        grid.attach(typeLabel, 0, 0, 1, 1)
        grid.attach_next_to(self.typeWidget, typeLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.valueLabel, typeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.valueWidget, self.valueLabel, Gtk.PositionType.RIGHT, 1, 1)

        buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        addButton = Gtk.Button("Add")
        applyButton = Gtk.Button("Apply")
        deleteButton = Gtk.Button("Delete")
        cancelButton = Gtk.Button("Cancel")

        addButton.connect("clicked", self.addPower)
        applyButton.connect("clicked", self.applyPower)
        deleteButton.connect("clicked", self.deletePower)
        cancelButton.connect("clicked", self.destroy)

        buttonBox.pack_start(addButton, False, False, 0)
        buttonBox.pack_start(deleteButton, False, False, 0)
        buttonBox.pack_start(applyButton, False, False, 0)
        buttonBox.pack_start(cancelButton, False, False, 0)

        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        menuBox.pack_start(grid, False, False, 0)
        menuBox.pack_start(buttonBox, False, False, 0)

        self.box.pack_start(self.tree, True, True, 0)
        self.box.pack_start(menuBox, False, False, 0)

    def addPower(self, widget):
        if not entryExist(self.store, self.typeWidget.get_active_text(), 0):
            self.store.append([self.typeWidget.get_active_text(),\
                               self.valueWidget.get_text()])

    def deletePower(self, widget):
        selection = self.tree.get_selection()
        if selection == None:
            return

        model, paths = selection.get_selected_rows()

        for path in paths[::-1]:
            i = self.store.get_iter(path)
            self.store.remove(i)

    def editRenderer(self, renderer, path, text, value):
        model = self.store
        iterModel = model.get_iter(path)
        if value == "Value":
            text = self.getValue(model[iterModel][0], text)
            model[iterModel][1] = text
        elif value == "Type":
            model[iterModel][0] = text

    def applyPower(self, widget):
        copyStore(self.store, self.power.store)

    def getValue(self, name, value):
        t = None

        iterPower = self.editPower.store.get_iter_first()
        while iterFirst != None:
            if name == self.editPower.store[iterPower][0]:
                t = self.editPower.store[iterPower][2]
                break

        if t == "Float":
            try:
                value = str(float(value))
            except ValueError:
                value = "0.0"

        elif t == "Int":
            try:
                value = str(int(float(value)))
            except ValueError:
                value = "0"

        elif t == "Bool":
            try:
                value = str(int(int(value) != 0))
            except ValueError:
                value = "0"

        return value

    def run(self):
        self.window = Gtk.Window(title="Power editor")
        self.window.add(self.box)
        self.window.connect("destroy", self.destroy)
        self.window.show_all()
        self.window.set_modal(True)

    def destroy(self, window):
        self.window.remove(self.box)
        self.window.destroy()
        copyStore(self.power.store, self.store)

class Power:
    def __init__(self):
        self.store = Gtk.ListStore(str, str)
