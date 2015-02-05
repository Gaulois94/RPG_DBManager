from gi.repository import Gtk

def addEntryInComboBoxText(comboBoxText):
    typeText = comboBoxText.get_active_text()
    addTextInComboBoxText(comboBoxText, typeText)

def addTextInComboBoxText(comboBoxText, typeText):
    if typeText == "":
        return

    b = False
    typeModel = comboBoxText.get_model()
    modelIter = typeModel.get_iter_first()

    while modelIter != None:
        if typeModel[modelIter][0] == typeText:
            b = True
            break
        modelIter = typeModel.iter_next(modelIter)

    if not b:
        comboBoxText.append_text(typeText)

def quitWindow(self, window):
    window.destroy()

def columnListStore(store, columnID):
    value = list()

    iterStore = store.get_iter_first()
    while iterStore != None:
        value.append(store[iterStore][columnID])
        iterStore = store.iter_next(iterStore)
    return value

def copyStore(source, destination):
    destination.clear()
    iterSource = source.get_iter_first()

    while iterSource != None:
        destination.append(source[iterSource])
        iterSource = source.iter_next(iterSource)

def replaceNone(l):
    for i in range(len(l)):
        if l[i] == None:
            l[i] = ""
