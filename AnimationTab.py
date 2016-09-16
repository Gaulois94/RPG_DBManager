from gi.repository import Gtk
from globalVar import *
from functions import *
from TreeTab import TreeTab
import databaseFunctions
import AnimTypeModel

class AnimationTab(TreeTab):
    def __init__(self, window):
        self.databaseWindow = window
        store = Gtk.TreeStore(*([int] + [x[1] for x in animModel]))
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
                renderer.connect("edited", self.editAnimRenderer, i)

            column = Gtk.TreeViewColumn(value[0], renderer, text=i+1)
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
        pathLabel = Gtk.Label("Image path")

        self.unitWidget = Gtk.ComboBox.new_with_model(AnimTypeModel.unitStore)
        cell            = Gtk.CellRendererText()
        self.unitWidget.pack_start(cell, False)
        self.unitWidget.add_attribute(cell, "text", 0)

        self.nameWidget = Gtk.Entry()

        self.typeWidget = Gtk.ComboBox.new_with_model(AnimTypeModel.animTypeModel)
        cell            = Gtk.CellRendererText()
        self.typeWidget.pack_start(cell, True)
        self.typeWidget.add_attribute(cell, "text", 0)

        self.imageEntered = Gtk.Entry()
        self.imageEntered.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FILE)
        self.imageEntered.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)
        self.imageEntered.connect("icon-press", self.openImage)

        valueGrid = Gtk.Grid(orientation = Gtk.Orientation.VERTICAL)
        valueGrid.attach(unitLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.unitWidget, unitLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(nameLabel, unitLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(typeLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.typeWidget, typeLabel, Gtk.PositionType.RIGHT, 3, 1)
        valueGrid.attach_next_to(pathLabel, typeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.imageEntered, pathLabel, Gtk.PositionType.RIGHT, 3, 1)

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
            parent = self.store.append(None, [-1, values[1], "", "", ""])

        databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UnitAnim", [str(self.idEntry), databaseFunctions.getUnitID(self.databaseWindow.database, values[1])] + values[2:])
        if values[3] == "Static":
            for orientation in ["TOP", "BOTTOM", "LEFT", "RIGHT"]:
                databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UnitStaticAnim", [str(self.idEntry), orientation] + self.getDefaultStaticValue())

        TreeTab.addEntry(self, parent)

    def getInsertValue(self):
        return [self.idEntry, str(AnimTypeModel.unitStore[self.unitWidget.get_active_iter()][0]),\
                self.nameWidget.get_text(),\
                AnimTypeModel.animTypeModel[self.typeWidget.get_active_iter()][0],\
                self.imageEntered.get_text()]

    def setAttributes(self, button):
        selection = self.tree.get_selection()
        if selection == None:
            return

        animModel, paths = selection.get_selected_rows()
        if len(paths) == 0:
            return

        if animModel[paths[0]][3] == "Static":
            self.setStaticAttributes(animModel, paths)
        else:
            self.setDynamicAttributes(animModel, paths)


    def setStaticAttributes(self, animModel, paths):

        animID = animModel[paths[0]][0]

        window = Gtk.Window(title = "Static animation")
        window.set_modal(True)

        #define the model
        print("setAttributes : anim ID = " + str(animID))
        model = Gtk.ListStore(str, int, int, int, int, int, int, int, int)
        for orientation in ["TOP", "BOTTOM", "LEFT", "RIGHT"]:
            cursor = databaseFunctions.getStaticAnimValue(self.databaseWindow.database, animID, orientation)
            for row in cursor:
                model.append(row)

        mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

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

        #Define labels
        posLabel  = Gtk.Label("Position")
        sizeLabel = Gtk.Label("Size per tile")
        padLabel  = Gtk.Label("Spacement between tiles")
        nLabel    = Gtk.Label("Number of tiles")
        nXLabel   = Gtk.Label("Tiles per row")
        #the x label
        xPosLabel = Gtk.Label("x")
        xSizeLabel = Gtk.Label("x")
        xPadLabel  = Gtk.Label("x")

        #The adjustment for all SpinButton		
        posXAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        posYAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        sizeXAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        sizeYAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        padXAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        padYAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        nAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        nXAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        
        #The spin button
        posXWidget = Gtk.SpinButton()
        posYWidget = Gtk.SpinButton()
        sizeXWidget = Gtk.SpinButton()
        sizeYWidget = Gtk.SpinButton()
        padXWidget = Gtk.SpinButton()
        padYWidget = Gtk.SpinButton()
        nWidget = Gtk.SpinButton()
        nXWidget = Gtk.SpinButton()
        
        #set the adjustment
        posXWidget.set_adjustment(posXAdjustment)
        posYWidget.set_adjustment(posYAdjustment)
        sizeXWidget.set_adjustment(sizeXAdjustment)
        sizeYWidget.set_adjustment(sizeYAdjustment)
        padXWidget.set_adjustment(padXAdjustment)
        padYWidget.set_adjustment(padYAdjustment)
        nWidget.set_adjustment(nAdjustment)
        nXWidget.set_adjustment(nXAdjustment)
        
        #Add these widgets to the grid
        mainGrid = Gtk.Grid(orientation = Gtk.Orientation.VERTICAL);
        
        mainGrid.attach(posLabel, 0, 0, 1, 1)
        mainGrid.attach_next_to(posXWidget, posLabel, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(xPosLabel, posXWidget, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(posYWidget, xPosLabel, Gtk.PositionType.RIGHT, 1, 1)
        
        mainGrid.attach_next_to(sizeLabel, posLabel, Gtk.PositionType.BOTTOM, 1, 1)
        mainGrid.attach_next_to(sizeXWidget, sizeLabel, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(xSizeLabel, sizeXWidget, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(sizeYWidget, xSizeLabel, Gtk.PositionType.RIGHT, 1, 1)
        
        mainGrid.attach_next_to(padLabel, sizeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        mainGrid.attach_next_to(padXWidget, padLabel, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(xPadLabel, padXWidget, Gtk.PositionType.RIGHT, 1, 1)
        mainGrid.attach_next_to(padYWidget, xPadLabel, Gtk.PositionType.RIGHT, 1, 1)
        
        mainGrid.attach_next_to(nLabel, padLabel, Gtk.PositionType.BOTTOM, 1, 1)
        mainGrid.attach_next_to(nWidget, nLabel, Gtk.PositionType.RIGHT, 3, 1)
        
        mainGrid.attach_next_to(nXLabel, nLabel, Gtk.PositionType.BOTTOM, 1, 1)
        mainGrid.attach_next_to(nXWidget, nXLabel, Gtk.PositionType.RIGHT, 3, 1)
        
        buttonBox = Gtk.Box()
        replaceButton = Gtk.Button(label="Replace")
        replaceButton.connect("clicked", self.replaceStatic, {"animID" : animID, "treeView" : view,\
                                                              "posX" : posXWidget, "posY" : posYWidget,\
                                                              "sizeX" : sizeXWidget, "sizeY" : sizeYWidget,\
                                                              "padX" : padXWidget, "padY" : padYWidget,\
                                                              "n" : nWidget, "nX" : nXWidget})
        buttonBox.add(replaceButton)

        mainBox.add(mainGrid)
        mainBox.add(buttonBox)

        window.add(mainBox)
        window.set_size_request(1024, 300)
        window.show_all()

    def setDynamicValue(self, model, paths):
        pass

    def editAttributeValue(self, renderer, path, text, model, animID, index):
        try:
            text = int(text)
        except:
            text = 0

        model[path][index] = text
        databaseFunctions.setStaticAnimEntry(self.databaseWindow.database, animID, model[path][0], staticModel[index], text)

    def getDefaultStaticValue(self):
        return ["0", "0", "0", "0", "0", "0", "0", "0"]
		
    def replaceStatic(self, button, widgets):
        selection = widgets["treeView"].get_selection()
        if selection == None:
            return

        animModel, paths = selection.get_selected_rows()
        if len(paths) == 0:
            return

        path = paths[0]
        orientation = animModel[path][staticModel.index("orientation")]

        values = [widgets["posX"].get_value(), widgets["posY"].get_value(),\
                  widgets["sizeX"].get_value(), widgets["sizeY"].get_value(),\
                  widgets["padX"].get_value(), widgets["padY"].get_value(),\
                  widgets["n"].get_value(), widgets["nX"].get_value()]

        values = [int(v) for v in values]

        start = staticModel.index("x")
        for i in range(start, start+len(values)):
            animModel[path][i] = values[i-start]

        databaseFunctions.setStaticAnimEntries(self.databaseWindow.database, widgets["animID"], orientation,
                                               ["x", "y", "sizeX", "sizeY", "padX", "padY", "n", "nX"],\
                                               values)

    def openImage(self, entry, pos, event):
        path = self.databaseWindow.fileManager.selectPath("Choose an image", "image")
        if path:
            entry.set_text(path)

    def editAnimRenderer(self, renderer, path, text, index):
        try:
            text = animModel[index][1](text)
        except:
            text = 0

        self.store[path][index+1] = text
        databaseFunctions.setDatabaseEntry(self.databaseWindow.database, "ANIM", str(self.store[path][0]), animModel[index][2], text)
