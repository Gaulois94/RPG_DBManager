from Tab import Tab

class TreeTab(Tab):
    def __init__(self, store):
        Tab.__init__(self, store)

    def addEntry(self, parent):
        v = self.getInsertValue()

        self.store.append(parent, v)
        self.idEntry = self.idEntry + 1
