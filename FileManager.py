from gi.repository import Gtk
from os import path as osPath
import os
from globalVar import *
from databaseFunctions import *

class FileManager:
    def __init__(self, path=None):
        self.path = path

    def saveAs(self, databaseWindow, unitTab, handlePower):
        path = self.selectPath("Where to save the database ?")
        if path == None:
            return

        save = True
        if osPath.exists(path):
            messageDialog = Gtk.MessageDialog(databaseWindow, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "The file already exists. Are you sure you want to save ?")

            save = messageDialog.run()
            messageDialog.destroy()

        if save == Gtk.ResponseType.YES or save == True:
            os.remove(path)
            self.saveFile(databaseWindow, unitTab, handlePower, path)

        return self.path

    def selectPath(self, message, mime=None):
        fileChooserDialog = Gtk.FileChooserDialog(message, databaseWindow, \
                            Gtk.FileChooserAction.SAVE, (Gtk.STOCK_SAVE, Gtk.ResponseType.OK, \
                            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        if mime:
            self.setFilter(fileChooserDialog, mime)

        response = fileChooserDialog.run()
        fileName = None
        if response == Gtk.ResponseType.OK:
            fileName = fileChooserDialog.get_filename()
        fileChooserDialog.destroy()
        return fileName

    def saveFile(self, windowDatabase, unitTab, animTab, handlePower, path=None):
        if path == None:
            if self.path == None:
                self.path = self.selectPath("Where to save the database ?")

                if self.path == None:
                    return
                elif osPath.exists(self.path):
                    os.remove(self.path)

                connection = initDatabase(self.path)
                recreateDatabase(windowDatabase.classTab, unitTab, animTab, handlePower, connection)
                windowDatabase.database.close()
                windowDatabase.database = connection
            else:
                saveDatabase(windowDatabase.database)
        else:
            if path == self.path:
                saveDatabase(windowDatabase.database)
            else:
                self.path = path
                connection = initDatabase(self.path)
                recreateDatabase(windowDatabase.classTab, unitTab, animTab, handlePower, connection)
                windowDatabase.database.close()
                windowDatabase.database = connection

    def openFile(self, unitTab, animTab, handlePower, windowDatabase):
        path = self.selectPath("Choose a file", "db")
        if path != None:
            unitTab.clearEntries()
            handlePower.clearEntries()
            self.path = path
            windowDatabase.database.close()
            windowDatabase.database = loadDatas(windowDatabase.classTab, unitTab, animTab, handlePower, path)
            if windowDatabase.sqlFile:
                windowDatabase.sqlFile.close()
                windowDatabase.sqlFile = None
            self.path = path

    def setFilter(self, dialog, mime):
        if mime == "db":
            filterDB = Gtk.FileFilter()
            filterDB.set_name("Database File")
            filterDB.add_mime_type("application/x-sqlite3")
            dialog.add_filter(filterDB)

        elif mime=="image":
            filterImage = Gtk.FileFilter()
            filterImage.set_name("Image File")
            filterImage.add_mime_type("image/png")
            filterImage.add_mime_type("image/jpeg")
            filterImage.add_mime_type("image/bmp")
            dialog.add_filter(filterImage)

