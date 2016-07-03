from gi.repository import Gtk

class Tab(Gtk.Box):
    def __init__(self, store):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        self.store     = store
        self.tree      = Gtk.TreeView(model = self.store)
        self.tree.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
        scrollWindow   = Gtk.ScrolledWindow()
        scrollWindow.add(self.tree)

        self.idEntry   = 0

        self.pack_start(scrollWindow, True, True, 0)
        self.pack_start(self.createHandleManager(), False, False, 0)

    def addEntry(self):
        v = self.getInsertValue()
        if v:
            self.store.append(v)

        self.idEntry = self.idEntry+1

    def deleteEntry(self, modelStr):
        selection = self.tree.get_selection()
        if selection == None:
            return

        model, paths     = selection.get_selected_rows()

        for path in paths[::-1]:
            i = model.get_iter(path)
            model.remove(i)

    def clearEntries(self):
        self.store.clear()
        self.idEntry = 0

    def resetID(self, modelStr):
        model        = self.store
        treeIter     = model.get_iter_first()
        idIndex      = modelStr.index("ID")
        self.idEntry = 0
        while treeIter != None:
            self.idEntry = self.idEntry+1
            self.store[treeIter][idIndex] = str(self.idEntry)
            treeIter = model.iter_next(treeIter)

        print(resetID)

    def replaceEntries(self, modelStr):
        selection = self.tree.get_selection()
        if selection == None:
            return

        model, paths = selection.get_selected_rows()

        for path in paths[::-1]:
            i = model.get_iter(path)
            values = self.getInsertValue()
            idIndex = modelStr.index("ID")
            values[idIndex] = model[i][idIndex]

            model.insert_after(i, values)
            model.remove(i)

tree = property(lambda self : self.tree)
