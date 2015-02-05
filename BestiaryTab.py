from gi.repository import Gtk
from globalVar import *
from functions import *
from Tab import Tab

class BestiaryTab(Tab):
    def __init__(self):
        store     = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str, str, str)
        Tab.__init__(self, store)

        for i, value in enumerate(bestiaryModel):
            renderer = None
            if value == "Type":
                renderer = Gtk.CellRendererCombo()
                renderer.set_property("has-entry", True)
                renderer.set_property("model", self.typeWidget.get_model())
                renderer.set_property("text-column", 0)
            else:
                renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            renderer.connect("edited", self.editRenderer, value)
            column   = Gtk.TreeViewColumn(value, renderer, text=i)
            column.set_resizable(True)
            column.set_expand(True)
            self.tree.append_column(column)

    def createHandleManager(self):
        grid      = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        grid.set_halign(Gtk.Align.END)
        grid.set_valign(Gtk.Align.END)

        typeLabel              = Gtk.Label("Type")
        nameLabel              = Gtk.Label("Name")
        pvMPLabel              = Gtk.Label("PV / MP")
        adAPLabel              = Gtk.Label("AD / AP")
        prMRLabel              = Gtk.Label("PR / MR")
        sizeLabel              = Gtk.Label("Size")
        weightLabel            = Gtk.Label("Weight")
        speedLabel             = Gtk.Label("Speed")
        attackSpeedLabel       = Gtk.Label("Attack Speed")
        descriptionLabel       = Gtk.Label("Description")

        xPVMPLabel             = Gtk.Label("x")
        xADAPLabel             = Gtk.Label("x")
        xPRMRLabel             = Gtk.Label("x")

        pvAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        mpAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        adAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        apAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        prAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        mrAdjustment          = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        sizeAdjustment        = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        weightAdjustment      = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        speedAdjustment       = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)
        attackSpeedAdjustment = Gtk.Adjustment(0, 0, 1000000, 1, 10, 0)

        self.typeWidget        = Gtk.ComboBoxText.new_with_entry()
        self.nameWidget        = Gtk.Entry()

        self.pvWidget          = Gtk.SpinButton()
        self.mpWidget          = Gtk.SpinButton()
        self.adWidget          = Gtk.SpinButton()
        self.apWidget          = Gtk.SpinButton()
        self.prWidget          = Gtk.SpinButton()
        self.mrWidget          = Gtk.SpinButton()
        self.sizeWidget        = Gtk.SpinButton(digits=2)
        self.sizeWidget.set_wrap(False)
        self.weightWidget      = Gtk.SpinButton(digits=2)
        self.weightWidget.set_wrap(False)
        self.speedWidget       = Gtk.SpinButton(digits=2)
        self.speedWidget.set_wrap(False)
        self.attackSpeedWidget = Gtk.SpinButton(digits=2)
        self.attackSpeedWidget.set_wrap(False)

        self.pvWidget.set_adjustment(pvAdjustment)
        self.mpWidget.set_adjustment(mpAdjustment)
        self.adWidget.set_adjustment(adAdjustment)
        self.apWidget.set_adjustment(apAdjustment)
        self.prWidget.set_adjustment(prAdjustment)
        self.mrWidget.set_adjustment(mrAdjustment)
        self.sizeWidget.set_adjustment(sizeAdjustment)
        self.weightWidget.set_adjustment(weightAdjustment)
        self.speedWidget.set_adjustment(speedAdjustment)
        self.attackSpeedWidget.set_adjustment(attackSpeedAdjustment)

        scrollDescriptionWidget = Gtk.ScrolledWindow()
        self.descriptionWidget  = Gtk.TextView()
        self.descriptionWidget.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        scrollDescriptionWidget.add(self.descriptionWidget)
        scrollDescriptionWidget.set_size_request(50, 100)

        valueGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        valueGrid.attach(typeLabel, 0, 0, 1, 1)
        valueGrid.attach_next_to(self.typeWidget, typeLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(nameLabel, typeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.nameWidget, nameLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(pvMPLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
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

        valueGrid.attach_next_to(sizeLabel, prMRLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.sizeWidget, sizeLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(weightLabel, sizeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.weightWidget, weightLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(speedLabel, weightLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.speedWidget, speedLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(attackSpeedLabel, speedLabel, Gtk.PositionType.BOTTOM, 1, 1)
        valueGrid.attach_next_to(self.attackSpeedWidget, attackSpeedLabel, Gtk.PositionType.RIGHT, 3, 1)

        valueGrid.attach_next_to(descriptionLabel, attackSpeedLabel, Gtk.PositionType.BOTTOM, 1, 1)
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
        Tab.addEntry(self)
        addEntryInComboBoxText(self.typeWidget)

    def getInsertValue(self):
        descriptionBuffer = self.descriptionWidget.get_buffer()
        return [self.typeWidget.get_active_text(),\
                str(self.idEntry),\
                self.nameWidget.get_text(),\
                str(int(self.pvWidget.get_value())), str(int(self.mpWidget.get_value())),\
                str(int(self.adWidget.get_value())), str(int(self.apWidget.get_value())),\
                str(int(self.prWidget.get_value())), str(int(self.mrWidget.get_value())),\
                str(float(self.sizeWidget.get_value())),\
                str(float(self.weightWidget.get_value())),\
                str(float(self.speedWidget.get_value())),\
                str(float(self.attackSpeedWidget.get_value())),\
                descriptionBuffer.get_text(descriptionBuffer.get_start_iter(), descriptionBuffer.get_end_iter(), False)\
               ]

    def resetEntries(self, widget):
        self.nameWidget.set_text("")
        self.pvWidget.set_value(0)
        self.mpWidget.set_value(0)
        self.adWidget.set_value(0)
        self.apWidget.set_value(0)
        self.prWidget.set_value(0)
        self.mrWidget.set_value(0)
        self.weightWidget.set_value(0)
        self.speedWidget.set_value(0)
        self.attackSpeedWidget.set_value(0)

    def deleteEntry(self):
        Tab.deleteEntry(self, bestiaryModel)

    def replaceEntries(self, widget):
        Tab.replaceEntries(self, bestiaryModel)

    def editRenderer(self, renderer, path, text, value):
        if value in ["PV", "MP", "AD", "AP", "PR", "MR"]:
            try:
                text = str(int(float(text)))
            except:
                text = "0"
        elif value in ["Size", "Weight", "Speed", "Attack Speed"]:
            try:
                text = str(float(text))
            except:
                text = "0.0"

        elif value == "Type":
            addTextInComboBoxText(self.typeWidget, text)

        index = bestiaryModel.index(value)
        self.store[path][index] = text
