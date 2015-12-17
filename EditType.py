from gi.repository import Gtk
from functions import *
import globalVar
from ArmoryTab import ArmoryTab
from BestiaryTab import BestiaryTab

class EditType:
    def __init__(self, bestiaryTab, armoryTab):
        self.bestiaryTab = bestiaryTab
        self.armoryTab   = armoryTab
        self.bestiaryTree       = Gtk.TreeView(model = bestiaryTab.typeWidget.get_model())
        self.armoryTree         = Gtk.TreeView(model = armoryTab.typeWidget.get_model())

        bestiaryRenderer = Gtk.CellRendererText()
        bestiaryColumn   = Gtk.TreeViewColumn("Bestiary Type", bestiaryRenderer, text=0)
        self.bestiaryTree.append_column(bestiaryColumn)

        armoryRenderer = Gtk.CellRendererText()
        armoryColumn   = Gtk.TreeViewColumn("Armory Type", armoryRenderer, text=0)
        self.armoryTree.append_column(armoryColumn)

        boxTree = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxTree.pack_start(self.bestiaryTree, True, True, 2)
        boxTree.pack_start(self.armoryTree, True, True, 2)

        widgetGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        classLabel = Gtk.Label("Class")
        nameValue = Gtk.Label("Name")

        self.classWidget = Gtk.ComboBoxText.new()
        self.classWidget.append_text("Bestiary")
        self.classWidget.append_text("Armory")

        self.nameWidget =  Gtk.Entry()

        widgetGrid.attach(classLabel, 0, 0, 1, 1)
        widgetGrid.attach_next_to(self.classWidget, classLabel, Gtk.PositionType.RIGHT, 3, 1)
        widgetGrid.attach_next_to(nameValue, classLabel, Gtk.PositionType.BOTTOM, 1, 1)
        widgetGrid.attach_next_to(self.nameWidget, nameValue, Gtk.PositionType.RIGHT, 3, 1)

        boxButton = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        addButton = Gtk.ToolButton()
        addButton.set_stock_id(Gtk.STOCK_NEW)

        moveDownButton = Gtk.ToolButton()
        moveDownButton.set_stock_id(Gtk.STOCK_GO_DOWN)

        moveUpButton = Gtk.ToolButton()
        moveUpButton.set_stock_id(Gtk.STOCK_GO_UP)

        deleteButton = Gtk.ToolButton()
        deleteButton.set_stock_id(Gtk.STOCK_DELETE)

        boxButton.pack_start(addButton, True, True, 0)
        boxButton.pack_start(moveDownButton, True, True, 0)
        boxButton.pack_start(moveUpButton, True, True, 0)
        boxButton.pack_start(deleteButton, True, True, 0)

        addButton.connect("clicked", self.addValue)
        moveDownButton.connect("clicked", self.buttonHandler, "moveDown")
        moveUpButton.connect("clicked", self.buttonHandler, "moveUp")
        deleteButton.connect("clicked", self.buttonHandler, "delete")

        boxHandler = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxHandler.pack_start(widgetGrid, False, False, 0)
        boxHandler.pack_start(boxButton, True, True, 0)

        boxHandler.set_halign(Gtk.Align.END)
        boxHandler.set_valign(Gtk.Align.END)

        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(boxTree, True, True, 0)
        self.box.pack_start(boxHandler, False, False, 0)

    def editList(self):
        window = Gtk.Window()
        window.connect("delete-event", self.hideWindow)
        window.add(self.box)
        window.show_all()
        window.set_modal(True)

    def hideWindow(self, window, event):
        window.remove(self.box)
        window.destroy()

    def buttonHandler(self, window, value):
        tree = None
        typeIndex = None
        handlerModel = None
        deleteDatabase = None
        typeDeleteDatabase = None
    
        if self.bestiaryTree.has_focus():
            tree = self.bestiaryTree
            handlerModel = globalVar.databaseWindow.bestiaryTab.store
            typeIndex = globalVar.bestiaryModel.index("Type")
            typeDeleteDatabase = "BESTIARY_TYPE"
            deleteDatabase = "BESTIARY"

        elif self.armoryTree.has_focus():
            tree = self.armoryTree
            handlerModel = globalVar.databaseWindow.armoryTab.store
            typeIndex = globalVar.armoryModel.index("Type")
            typeDeleteDatabase = "EQUIPMENT_TYPE"
            deleteDatabase = "EQUIPMENT"

        else:
            return

        selection = tree.get_selection()
        if selection == None:
            return

        model, paths = selection.get_selected_rows()
        
        if value == "delete":
            for path in paths[::-1]:
                i = model.get_iter(path)

                handlerIter = handlerModel.get_iter_first()
                while handlerIter != None:
                    if handlerModel[handlerIter][typeIndex] == model[i][0]:
                        handlerModel[handlerIter][typeIndex] = ""
                    handlerIter = handlerModel.iter_next(handlerIter)

                databaseFunctions.deleteDatabaseEntry(self.databaseWindow.database, typeDeleteDatabase, model[i][0])
                model.remove(i)

    def addValue(self, widget):
        if self.nameWidget.get_text() != "":
            typeWidget = None
            if self.classWidget.get_active_text() == "Bestiary":
                typeWidget = self.bestiaryTab.typeWidget
                addTextInComboBoxText(typeWidget, self.nameWidget.get_text(), BestiaryTab.updateType, self.bestiaryTab)
            elif self.classWidget.get_active_text() == "Armory":
                typeWidget = self.armoryTab.typeWidget
                addTextInComboBoxText(typeWidget, self.nameWidget.get_text(), ArmoryTab.updateType, self.armoryTab)
