from gi.repository import Gtk
from globalVar import *
from functions import *
from TreeTab import TreeTab
import databaseFunctions
import AnimTypeModel

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

            elif value[0] == "Type":
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("model", AnimTypeModel.animTypeModel)
                renderer.set_property("text-column", 0)
                renderer.set_property("editable", False)
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

        self.unitWidget = Gtk.ComboBox.new_with_model(AnimTypeModel.unitStore)
        cell            = Gtk.CellRendererText()
        self.unitWidget.pack_start(cell, False)
        self.unitWidget.add_attribute(cell, "text", 0)

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
        setAttributeButton = Gtk.Button(label="Set attributes")
        setAttributeButton.connect("clicked", self.setAttributes)
        okButton  = Gtk.Button(label="Add")
        okButton.connect("clicked", self.addEntry)

        buttonBox.add(setAttributeButton)
        buttonBox.add(okButton)
        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        grid.add(valueGrid)
        grid.add(buttonBox)

        return grid

    def addEntry(self, widget):
        values = self.getInsertValue()
        parent = None

        treeIter = self.store.get_iter_first()
        while treeIter != None:
            if self.store[treeIter][0] == values[0]:
                parent = treeIter
                break
            treeIter = self.store.iter_next(treeIter)

        if parent == None:
            parent = self.store.append(None, [values[0], "", ""])

        databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UnitAnim", [str(self.idEntry), databaseFunctions.getUnitID(self.databaseWindow.database, values[0])] + values[1:])
        if values[2] == "Static":
            for orientation in ["TOP", "BOTTOM", "LEFT", "RIGHT"]:
                databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UnitStaticAnim", [str(self.idEntry), orientation] + self.getDefaultStaticValue())

        TreeTab.addEntry(self, parent)

    def getInsertValue(self):
        return [str(AnimTypeModel.unitStore[self.unitWidget.get_active_iter()][0]),\
                self.nameWidget.get_text(),\
                AnimTypeModel.animTypeModel[self.typeWidget.get_active_iter()][0]]

    def setAttributes(self, button):
        selection = self.tree.get_selection()
        if selection == None:
            return

        animModel, paths = selection.get_selected_rows()
        if len(paths) == 0:
            return

        animID = databaseFunctions.getAnimID(self.databaseWindow.database, animModel[paths[0]][0], animModel[paths[0]][1])

        window = Gtk.Window(title = "Static animation")
        window.set_modal(True)

        #define the model
        model = Gtk.ListStore(str, int, int, int, int, int, int, int, int)
        for orientation in ["TOP", "BOTTOM", "LEFT", "RIGHT"]:
            cursor = databaseFunctions.getStaticAnimValue(self.databaseWindow.database, animID, orientation)
            for row in cursor:
                model.append(row)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        #define the view
        view = Gtk.TreeView(model=model)
        view.get_selection().set_mode(Gtk.SelectionMode.SINGLE)

        for i, value in enumerate(["Orientation", "X position", "Y position", "Size X", "Size Y", "Pad X", "Pad Y", "Number of elements", "Number of elements per row"]):
            renderer = None
            if i == 0:
                renderer = Gtk.CellRendererText()
                renderer.set_property("editable", False)
            else:
                renderer = Gtk.CellRendererText()
                renderer.set_property("editable", True)
                renderer.connect("edited", self.editAttributeValue, model, animID, i)

            column = Gtk.TreeViewColumn(value, renderer, text = i)
            column.set_resizable(True)
            column.set_expand(True)
            view.append_column(column)
        scrollWindow   = Gtk.ScrolledWindow()
        scrollWindow.add(view)
        mainBox.pack_start(scrollWindow, True, True, 0)

        window.add(mainBox)
        window.set_size_request(1024, 300)
        window.show_all()

    def editAttributeValue(self, renderer, path, text, model, animID, index):
        try:
            text = int(text)
        except:
            text = 0

        model[path][index] = text
        databaseFunctions.setStaticAnimEntry(self.databaseWindow.database, animID, model[path][0], staticModel[index], text)

    def getDefaultStaticValue(self):
        return ["0", "0", "0", "0", "0", "0", "0", "0"]
