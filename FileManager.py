from gi.repository import Gtk
from os import path as osPath
import os
from globalVar import *
from databaseFunctions import *

class FileManager:
    def __init__(self, path=None):
        self.path = path

    def saveAs(self, databaseWindow, bestiaryTab, armoryTab, handlePower):
        path = self.selectPath("Where to save the database ?")
        if path == None:
            return

        save = True
        if osPath.exists(path):
            messageDialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
            messageDialog.set_markup("The file already exists. Are you sur you want to save ?")
            save = messageDialog.run()

        messageDialog.destroy()
        if save == Gtk.ResponseType.YES:
            self.saveFile(databaseWindow, bestiaryTab, armoryTab, handlePower, path)

        return self.path

    def selectPath(self, message):
        fileChooserDialog = Gtk.FileChooserDialog(message, databaseWindow, \
                            Gtk.FileChooserAction.SAVE, (Gtk.STOCK_SAVE, Gtk.ResponseType.OK, \
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        response = fileChooserDialog.run()
        fileName = None
        if response == Gtk.ResponseType.OK:
            fileName = fileChooserDialog.get_filename()
        fileChooserDialog.destroy()
        return fileName

    def saveFile(self, windowDatabase, bestiaryTab, armoryTab, handlePower, path=None):
        if path == None:
            if self.path == None:
                self.path = self.selectPath("Where to save the database ?")

                if self.path == None:
                    return
                elif osPath.exists(self.path):
                    os.remove(self.path)

                connection = initDatabase(self.path)
                recreateDatabase(bestiaryTab, armoryTab, handlePower, connection)
                windowDatabase.database.close()
                windowDatabase.database = connection
            else:
                saveDatabase(windowDatabase.database)
        else:
            if path == self.path:
                saveDatabase(windowDatabase.database)
            else:
                self.path = path

    def openFile(self, bestiaryTab, armoryTab, handlePower, windowDatabase):
        path = self.selectPath("Choose a file")
        if path != None:
            bestiaryTab.clearEntries()
            armoryTab.clearEntries()
            handlePower.clearEntries()
            self.path = path
            windowDatabase.database.close()
            windowDatabase.database = loadDatas(bestiaryTab, armoryTab, handlePower, path)
            if windowDatabase.sqlFile:
                windowDatabase.sqlFile.close()
                windowDatabase.sqlFile = None
            self.path = path
