from gi.repository import Gtk
from databaseFunctions import *

def addEntryInComboBoxText(comboBoxText, f=None, *args):
    typeText = comboBoxText.get_active_text()
    addTextInComboBoxText(comboBoxText, typeText, f, *args)

def addTextInComboBoxText(comboBoxText, typeText, f=None, *args):
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
        if f != None:
            f(*args, typeText)

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
        nbColumn = source.get_n_columns()
        l = [source[iterSource][i] for i in range(nbColumn)]
        destination.append(l)
        iterSource = source.iter_next(iterSource)

def replaceNone(l):
    for i in range(len(l)):
        if l[i] == None:
            l[i] = ""

def entryExist(model, value, column):
    iterModel = model.get_iter_first()
    while iterModel != None:
        if model[iterModel][column] == value:
            return True
        iterModel = model.iter_next()
    return False
