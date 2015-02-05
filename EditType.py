from gi.repository import Gtk
import globalVar

class EditType:
    def __init__(self, bestiaryTypeWidget, armoryTypeWidget):
        self.bestiaryTypeWidget = bestiaryTypeWidget
        self.armoryTypeWidget   = armoryTypeWidget
        self.bestiaryTree       = Gtk.TreeView(model = bestiaryTypeWidget.typeWidget.get_model())
        self.armoryTree         = Gtk.TreeView(model = armoryTypeWidget.typeWidget.get_model())

        bestiaryRenderer = Gtk.CellRendererText()
        bestiaryColumn   = Gtk.TreeViewColumn("Bestiary Type", bestiaryRenderer, text=0)
        self.bestiaryTree.append_column(bestiaryColumn)

        armoryRenderer = Gtk.CellRendererText()
        armoryColumn   = Gtk.TreeViewColumn("Armory Type", armoryRenderer, text=0)
        self.armoryTree.append_column(armoryColumn)

        boxTree = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        boxTree.pack_start(self.bestiaryTree, True, True, 2)
        boxTree.pack_start(self.armoryTree, True, True, 2)

        boxButton = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        addButton = Gtk.ToolButton()
        addButton.set_stock_id(Gtk.STOCK_NEW)

        moveDownButton = Gtk.ToolButton()
        moveDownButton.set_stock_id(Gtk.STOCK_GO_DOWN)

        moveUpButton = Gtk.ToolButton()
        moveUpButton.set_stock_id(Gtk.STOCK_GO_UP)

        deleteButton = Gtk.ToolButton()
        deleteButton.set_stock_id(Gtk.STOCK_DELETE)

        boxButton.pack_start(addButton, False, False, 0)
        boxButton.pack_start(moveDownButton, False, False, 0)
        boxButton.pack_start(moveUpButton, False, False, 0)
        boxButton.pack_start(deleteButton, False, False, 0)

        deleteButton.connect("clicked", self.buttonHandler, "delete")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.pack_start(boxTree, True, True, 0)
        self.box.pack_start(boxButton, False, True, 0)

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
        if self.bestiaryTree.has_focus():
            tree = self.bestiaryTree
            handlerModel = globalVar.databaseWindow.bestiaryTab.store
            typeIndex = globalVar.bestiaryModel.index("Type")

        elif self.armoryTree.has_focus():
            tree = self.armoryTree
            handlerModel = globalVar.databaseWindow.armoryTab.store
            typeIndex = globalVar.armoryModel.index("Type")

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

                model.remove(i)
