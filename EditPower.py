from gi.repository import Gtk
import globalVar
from functions import *

class EditPower:
    def __init__(self):
        #Set the Store part 
        self.store    = Gtk.ListStore(str, bool, str, str, str)
        self.tree     = Gtk.TreeView(model=self.store)

        textRenderer  = Gtk.CellRendererText()

        textColumn    = Gtk.TreeViewColumn("Name", textRenderer, text=0)
        textColumn.set_resizable(True)
        textColumn.set_expand(True)
        self.tree.append_column(textColumn)

        toggleRenderer = Gtk.CellRendererToggle()
        toggleRenderer.connect("toggled", self.toggleRenderer)
        toggleRenderer.set_radio(False)
        toggleColumn   = Gtk.TreeViewColumn("Global Value", toggleRenderer, active=1)
        self.tree.append_column(toggleColumn)

        typeRenderer   = Gtk.CellRendererCombo()
        typeColumn     = Gtk.TreeViewColumn("Type", typeRenderer, text=2)
        typeColumn.set_resizable(True)
        self.tree.append_column(typeColumn)

        scrolledWindow = Gtk.ScrolledWindow()
        scrolledWindow.set_size_request(400, 150)
        scrolledWindow.add(self.tree)

        for i, value in enumerate(["Value", "Description"]):
            renderer   = Gtk.CellRendererText()
            column     = Gtk.TreeViewColumn(value, renderer, text=i+3)
            column.set_resizable(True)
            self.tree.append_column(column)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(scrolledWindow, True, True, 0)
        
        #Set the Widget part
        nameLabel        = Gtk.Label("Name")
        typeLabel        = Gtk.Label("Type")
        self.valueLabel  = Gtk.Label("Value")
        self.nameWidget  = Gtk.Entry()
        self.valueWidget = Gtk.Entry()
        self.typeWidget  = Gtk.ComboBoxText.new()

        for t in ["Int", "Float", "String", "Bool"]:
            self.typeWidget.append_text(t)
        self.typeWidget.set_active(0)

        typeRenderer.set_property("model", self.typeWidget.get_model())
        typeRenderer.set_property("editable", True)
        typeRenderer.set_property("text-column", 0)
        typeRenderer.connect("edited", self.changeTypeRenderer)

        self.globalValue = Gtk.CheckButton.new_with_label("Global Value")
        self.globalValue.set_active(True)
        self.globalValue.connect("toggled", self.changeGlobalValue)

        scrollDescriptionWidget = Gtk.ScrolledWindow()
        self.descriptionWidget  = Gtk.TextView()
        self.descriptionWidget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrollDescriptionWidget.add(self.descriptionWidget)
        scrollDescriptionWidget.set_size_request(50, 100)

        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        grid.attach(nameLabel, 0, 0, 1, 1)
        grid.attach(self.nameWidget, 1, 0, 1, 1)
        grid.attach(self.globalValue, 2, 0, 1, 1)

        grid.attach_next_to(typeLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.typeWidget, typeLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.valueLabel, typeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.valueWidget, self.valueLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(Gtk.Label("Description"), self.valueLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(scrollDescriptionWidget, self.valueWidget, Gtk.PositionType.BOTTOM, 2, 2)

        okButton  = Gtk.Button(label="Add")
        okButton.connect("clicked", self.addEntry)

        buttonBox = Gtk.Box()
        buttonBox.add(okButton)
        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.pack_start(grid, False, False, 0)
        vbox.pack_start(buttonBox, False, False, 0)

        self.box.pack_start(vbox, False, False, 0)


    def editList(self):
        window = Gtk.Window()
        window.connect("delete-event", self.hideWindow)
        window.add(self.box)
        window.show_all()
        window.set_modal(True)

        self.changeGlobalValue(self.globalValue)

    def changeGlobalValue(self, widget):
        if widget.get_active():
            self.valueLabel.show()
            self.valueWidget.show()
        else:
            self.valueLabel.hide()
            self.valueWidget.hide()

    def clearEntry(self):
        self.store.clear()

    def toggleRenderer(self, cellRenderer, path):
        self.store[path][1] = not self.store[path][1]

    def changeTypeRenderer(self, renderer, path, text):
        self.store[path][2] = text

    def addEntry(self, widget):
        if self.nameWidget.get_text() == "" or self.nameWidget.get_text() in columnListStore(self.store, 0):
            return 

        value = ""

        if self.typeWidget.get_active_text() == "Float":
            try:
                value = str(float(value))
            except ValueError:
                value = "0.0"

        elif self.typeWidget.get_active_text() == "Int":
            try:
                value = str(int(float(value)))
            except ValueError:
                value = "0"

        elif self.typeWidget.get_active_text() == "Bool":
            try:
                value = str(int(int(value) != 0))
            except ValueError:
                value = "0"

        descriptionBuffer = self.descriptionWidget.get_buffer()

        self.store.append([self.nameWidget.get_text(),
                           self.globalValue.get_active(),
                           self.typeWidget.get_active_text(),
                           value,
                           descriptionBuffer.get_text(descriptionBuffer.get_start_iter(), descriptionBuffer.get_end_iter(), False)])

    def hideWindow(self, window, event):
        window.remove(self.box)
        window.destroy()
