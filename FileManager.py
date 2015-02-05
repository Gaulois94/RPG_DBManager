from gi.repository import Gtk
from os import path as osPath
import os
from globalVar import *
from databaseFunctions import *

class FileManager:
    def __init__(self, path=None):
        self.path = path

    def saveAs(self, bestiaryTab, armoryTab, handlePower):
        path = self.selectPath()
        if path == None:
            return

        save = True
        if osPath.exists(path):
            messageDialog = Gtk.MessageDialog(type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO)
            messageDialog.set_markup("The file already exists. Are you sur you want to save ?")
            save = messageDialog.run()

        messageDialog.destroy()
        if save == Gtk.ResponseType.YES:
            self.saveFile(database, bestiaryTab, armoryTab, handlePower, path)

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

    def saveFile(self, bestiaryTab, armoryTab, handlePower, path=None):
        if path == None:
            if self.path == None:
                self.path = self.selectPath("Where to save the database ?")

        path = self.path

        if path == None:
            return
        elif osPath.exists(path):
            os.remove(path)

        saveDatabase(bestiaryTab, armoryTab, handlePower, path)

    def openFile(self, bestiaryTab, armoryTab, handlePower):
        path = self.selectPath("Choose a file")
        if path != None:
            bestiaryTab.clearEntry()
            armoryTab.clearEntry()
            handlePower.clearEntry()
            self.path = path
            loadDatas(bestiaryTab, armoryTab, handlePower, path)  
            self.path = path
