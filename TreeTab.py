from Tab import Tab

class TreeTab(Tab):
    def __init__(self, store):
        Tab.__init__(self, store)

    def addEntry(self):
        v = self.getInsertValue()
        p = self.getParent()

        self.store.append(p, v)
        self.idEntry = self.idEntry + 1

    def getParent(self):
        return None
