from gi.repository import Gtk
from globalVar import *
from functions import *
from TreeTab import TreeTab
import databaseFunctions
import AnimTypeModel

class UnitTab(TreeTab):
    def __init__(self, window):
        self.databaseWindow = window
        store     = Gtk.TreeStore(*[x[1] for x  in unitModel])
        TreeTab.__init__(self, store)

        for i, value in enumerate(unitModel):
            renderer = None

            if value[0] == "Type Name":
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("model", window.classTab.store)
                renderer.set_property("text-column", 0)
                renderer.set_property("editable", True)
                renderer.connect("edited", self.editRenderer, i)

            elif value[0] == "Winged":
                renderer = Gtk.CellRendererToggle()
                renderer.set_property("activatable", True)
                renderer.connect("toggled", self.toggleRenderer, i)

            else:
                renderer = Gtk.CellRendererText()
                if value[0] != "ID":
                    renderer.set_property("editable", True)
                renderer.connect("edited", self.editRenderer, i)
            column   = Gtk.TreeViewColumn(value[0], renderer, text=i)
            column.set_resizable(True)
            column.set_expand(True)
            self.tree.append_column(column)

    def createHandleManager(self):
        grid      = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        grid.set_halign(Gtk.Align.END)
        grid.set_valign(Gtk.Align.END)

        classLabel             = Gtk.Label("Type")
        nameLabel              = Gtk.Label("Name")
        wingedLabel            = Gtk.Label("Winged")
        levelLabel             = Gtk.Label("Level")
        priceLabel             = Gtk.Label("Price")
        occupationLabel        = Gtk.Label("Occupation")
        pvMPLabel              = Gtk.Label("PV / MP")
        adAPLabel              = Gtk.Label("AD / AP")
        prMRLabel              = Gtk.Label("PR / MR")
        movingLabel            = Gtk.Label("Moving")
        attackSpeedLabel       = Gtk.Label("Attack Speed")
        moveStatsLabel         = Gtk.Label("Move Stats")
        descriptionLabel       = Gtk.Label("Description")

        xPVMPLabel             = Gtk.Label("x")
        xADAPLabel             = Gtk.Label("x")
        xPRMRLabel             = Gtk.Label("x")

        priceAdjustment       = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        levelAdjustment       = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        occupationAdjustment  = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        pvAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        mpAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        adAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        apAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        prAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        mrAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        movingAdjustment      = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        attackSpeedAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        movingStatsAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)

        self.classWidget       = Gtk.ComboBox.new_with_model(self.databaseWindow.classTab.store)
        cell                   = Gtk.CellRendererText()
        self.classWidget.pack_start(cell, True)
        self.classWidget.add_attribute(cell, "text", 0)

        self.classWidget.set_property("id-column", 0)
        self.nameWidget        = Gtk.Entry()
        self.wingedWidget      = Gtk.CheckButton()
        self.levelWidget       = Gtk.SpinButton()
        self.priceWidget       = Gtk.SpinButton()
        self.occupationWidget  = Gtk.SpinButton()

        self.pvWidget          = Gtk.SpinButton()
        self.mpWidget          = Gtk.SpinButton()
        self.adWidget          = Gtk.SpinButton()
        self.apWidget          = Gtk.SpinButton()
        self.prWidget          = Gtk.SpinButton()
        self.mrWidget          = Gtk.SpinButton()
        self.movingWidget      = Gtk.SpinButton()
        self.attackSpeedWidget = Gtk.SpinButton(digits=2)
        self.attackSpeedWidget.set_wrap(False)
        self.moveStatsWidget = Gtk.SpinButton(digits=2)
        self.moveStatsWidget.set_wrap(False)

        self.levelWidget.set_adjustment(levelAdjustment)
        self.priceWidget.set_adjustment(priceAdjustment)
        self.occupationWidget.set_adjustment(occupationAdjustment)
        self.pvWidget.set_adjustment(pvAdjustment)
        self.mpWidget.set_adjustment(mpAdjustment)
        self.adWidget.set_adjustment(adAdjustment)
        self.apWidget.set_adjustment(apAdjustment)
        self.prWidget.set_adjustment(prAdjustment)
        self.mrWidget.set_adjustment(mrAdjustment)
        self.movingWidget.set_adjustment(movingAdjustment)
        self.attackSpeedWidget.set_adjustment(attackSpeedAdjustment)
        self.moveStatsWidget.set_adjustment(movingStatsAdjustment)

        scrollDescriptionWidget = Gtk.ScrolledWindow()
        self.descriptionWidget  = Gtk.TextView()
        self.descriptionWidget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrollDescriptionWidget.add(self.descriptionWidget)
        scrollDescriptionWidget.set_size_request(50, 100)

        valueGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        valueGrid.attach(classLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.classWidget, classLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(nameLabel, classLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(wingedLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.wingedWidget, wingedLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(levelLabel, wingedLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.levelWidget, levelLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(priceLabel, levelLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.priceWidget, priceLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(occupationLabel, priceLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.occupationWidget, occupationLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(pvMPLabel, occupationLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.pvWidget, pvMPLabel, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(xPVMPLabel, self.pvWidget, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(self.mpWidget, xPVMPLabel, Gtk.PositionType.RIGHT, 1, 1)

        valueGrid.attach_next_to(adAPLabel, pvMPLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.adWidget, adAPLabel, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(xADAPLabel, self.adWidget, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(self.apWidget, xADAPLabel, Gtk.PositionType.RIGHT, 1, 1)

        valueGrid.attach_next_to(prMRLabel, adAPLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.prWidget, prMRLabel, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(xPRMRLabel, self.prWidget, Gtk.PositionType.RIGHT, 1, 1)
        valueGrid.attach_next_to(self.mrWidget, xPRMRLabel, Gtk.PositionType.RIGHT, 1, 1)

        valueGrid.attach_next_to(movingLabel, prMRLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.movingWidget, movingLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(attackSpeedLabel, movingLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.attackSpeedWidget, attackSpeedLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(moveStatsLabel, attackSpeedLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.moveStatsWidget, moveStatsLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(descriptionLabel, moveStatsLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(scrollDescriptionWidget, descriptionLabel, Gtk.PositionType.RIGHT, 3, 1)

        buttonBox = Gtk.Box()

        replaceButton = Gtk.Button(label="Replace")
        replaceButton.connect("clicked", self.replaceEntries)

        reinitButton  = Gtk.Button(label="Reinit")
        reinitButton.connect("clicked", self.resetEntries)

        okButton  = Gtk.Button(label="Add")
        okButton.connect("clicked", self.addEntry)

        buttonBox.add(replaceButton)
        buttonBox.add(reinitButton)
        buttonBox.add(okButton)

        buttonBox.set_halign(Gtk.Align.END)
        buttonBox.set_valign(Gtk.Align.END)

        grid.add(valueGrid)
        grid.add(buttonBox)

        return grid

    def addEntry(self, widget):
        values = self.getInsertValue()
        nameID = unitModel.index(("Name", str))
        model = self.tree.get_model()
        it = model.get_iter_first()
        while it != None:
            if model[it][nameID] == values[nameID]:
                return
            it = model.iter_next(it)
          
        if values:
            databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UNIT", [str(v) for v in values])
            parent = self.getParent()
            if parent != None:
                databaseFunctions.addDatabaseEntry(self.databaseWindow.database, "UnitTree", [str(model[parent][0]), str(values[0])])

        AnimTypeModel.unitStore.append([values[nameID]])
        TreeTab.addEntry(self, parent)

    def getInsertValue(self):
        descriptionBuffer = self.descriptionWidget.get_buffer()
        print(self.idEntry)
        return [self.idEntry,\
                str(self.databaseWindow.classTab.store[self.classWidget.get_active_iter()][0]),\
                self.nameWidget.get_text(),\
                self.wingedWidget.get_active(),\
                int(self.levelWidget.get_value()),\
                int(self.priceWidget.get_value()),\
                int(self.occupationWidget.get_value()),\
                int(self.pvWidget.get_value()), int(self.mpWidget.get_value()),\
                int(self.adWidget.get_value()), int(self.apWidget.get_value()),\
                int(self.prWidget.get_value()), int(self.mrWidget.get_value()),\
                int(self.movingWidget.get_value()),\
                self.attackSpeedWidget.get_value(),\
                self.moveStatsWidget.get_value(),\
                descriptionBuffer.get_text(descriptionBuffer.get_start_iter(), descriptionBuffer.get_end_iter(), False)\
               ]

    def getParent(self):
        selection = self.tree.get_selection()
        if selection == None:
            return None

        model, paths = selection.get_selected_rows()
        if len(paths) == 0:
            return None

        return model.get_iter(paths[-1])

    def resetEntries(self, widget):
        self.nameWidget.set_text("")
        self.levelWidget.set_value(0)
        self.typeWidget.set_value(0)
        self.priceWidget.set_value(0)
        self.occupationWidget.set_value(0)
        self.pvWidget.set_value(0)
        self.mpWidget.set_value(0)
        self.adWidget.set_value(0)
        self.apWidget.set_value(0)
        self.prWidget.set_value(0)
        self.mrWidget.set_value(0)
        self.weightWidget.set_value(0)
        self.movingWidget.set_value(0)
        self.attackSpeedWidget.set_value(0)

    def deleteEntry(self):
        TreeTab.deleteEntry(self, unitModel)

    def replaceEntries(self, widget):
        TreeTab.replaceEntries(self, unitModel)

    def toggleRenderer(self, renderer, path, index):
        self.store[path][index] = not self.store[path][index]
        renderer.set_active(self.store[path][index])
        print(self.store[path][index])
        databaseFunctions.setDatabaseEntry(self.databaseWindow.database, "UNIT", str(self.store[path][0]), unitModel[index][0], str(self.store[path][index]))

    def editRenderer(self, renderer, path, text, index):
        try:
            text = unitModel[index][1](text)
        except:
            text = 0

        self.store[path][index] = text
        databaseFunctions.setDatabaseEntry(self.databaseWindow.database, "UNIT", str(self.store[path][0]), unitModel[index][0], text)
