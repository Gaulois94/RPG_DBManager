from gi.repository import Gtk
from globalVar import *
from functions import *
from Tab import Tab
from Tab import Tab
import databaseFunctions

class ClassTab(Tab):
    def __init__(self, window):
        self.databaseWindow = window
        
        store     = Gtk.TreeStore(str)
        Tab.__init__(self, store)

        renderer = Gtk.CellRendererText()

        column   = Gtk.TreeViewColumn("Name", renderer, text=0)
        column.set_resizable(True)
        column.set_expand(True)
        self.tree.append_column(column)

    def createHandleManager(self):
        grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        grid.set_halign(Gtk.Align.END)
        grid.set_valign(Gtk.Align.END)

        nameLabel        = Gtk.Label("Name")
        classNameLabel   = Gtk.Label("Class Name")

        self.nameWidget  = Gtk.Entry()
        self.classWidget = Gtk.ComboBoxText(has_entry = True)

        valueGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        valueGrid.attach(classNameLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.classWidget, classNameLabel, Gtk.PositionType.RIGHT, 3, 1)
        valueGrid.attach_next_to(nameLabel, classNameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT,3, 1)

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
        values = self.getInsertValue()
        self.loadEntry(values, True)

    def getInsertValue(self):
        return [self.classWidget.get_active_text(),\
                self.nameWidget.get_text()]

    def resetEntries(self, widget):
        self.nameWidget.set_text("")

    def loadEntry(self, values, loadToDatabase):
        model = self.tree.get_model()
        it = model.get_iter_first()
        while it != None:
            if model[it][0] == values[1]:
                return
            it = model.iter_next(it)

        if values:
            it = model.get_iter_first()
            addClass = True

            while it != None:
                if model[it][0] == values[0]:
                    addClass = False
                    break
                it = model.iter_next(it)

            if addClass:
                if loadToDatabase:
                    databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "CLASS", [str(values[0])])
                self.store.append(None, [values[0]])
            if loadToDatabase:
                databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "TYPE", [str(v) for v in values])

        classPath = None
        it = model.get_iter_first()
        while it != None:
            if model[it][0] == values[0]:
                self.store.append(it, [values[1]])
                break
            it = model.iter_next(it)
