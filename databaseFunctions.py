from io import StringIO
from ArmoryTab import ArmoryTab
from BestiaryTab import BestiaryTab
from globalVar import *
from functions import *

import sqlite3 as sql

sqlInitDB = """
               CREATE TABLE ValueType(name VARCHAR(32) PRIMARY KEY);

               CREATE TABLE BestiaryType(name VARCHAR(32) PRIMARY KEY);

               CREATE TABLE Bestiary(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                      type        VARCHAR(32),
                                      name        VARCHAR(32) NOT NULL,
                                      modelPath   TEXT,
                                      pv          INTEGER,
                                      mp          INTEGER,
                                      ad          INTEGER,
                                      ap          INTEGER,
                                      pr          INTEGER,
                                      mr          INTEGER,
                                      size        FLOAT,
                                      weight      FLOAT,
                                      speed       FLOAT,
                                      attackSpeed FLOAT,
                                      description TEXT,
                                      FOREIGN KEY(type) REFERENCES BestiaryType(name));

               CREATE TABLE Capacity(name VARCHAR(32) PRIMARY KEY,
                                     isGlobal TINYINT NOT NULL,
                                     type  VARCHAR(32),
                                     value BLOB,
                                     description TEXT,
                                     FOREIGN KEY(type) REFERENCES ValueType(name));

               CREATE TABLE EquipmentClass(name VARCHAR(32) PRIMARY KEY);
                                   
               CREATE TABLE ItemType(name VARCHAR(32) PRIMARY KEY);
            
               CREATE TABLE Item(id INTEGER PRIMARY KEY,
                                  type VARCHAR(32) NOT NULL,
                                  FOREIGN KEY(type) REFERENCES ItemType(name));

               CREATE TABLE EquipmentType(name VARCHAR(32) PRIMARY KEY);

               CREATE TABLE Equipment(id          INTEGER PRIMARY KEY AUTOINCREMENT,
                                      class       VARCHAR(32) NOT NULL,
                                      type        VARCHAR(32),
                                      name        VARCHAR(32) NOT NULL,
                                      modelPath   TEXT,
                                      pv          INTEGER,
                                      mp          INTEGER,
                                      ad          INTEGER,
                                      ap          INTEGER,
                                      pr          INTEGER,
                                      mr          INTEGER,
                                      weight      FLOAT,
                                      speed       FLOAT,
                                      attackSpeed FLOAT,
                                      description TEXT,
                                      FOREIGN KEY(type) REFERENCES EquipmentType(name),
                                      FOREIGN KEY(class) REFERENCES EquipmentClass(name),
                                      FOREIGN KEY(id)   REFERENCES Item(id)
                                      ON DELETE CASCADE);

               CREATE TABLE EquipmentCapacity(id     INTEGER,
                                              type   VARCHAR(32),
                                              value  BLOB,
                                              FOREIGN KEY(id) REFERENCES Equipment(id)
                                              ON DELETE CASCADE,
                                              FOREIGN KEY(type) REFERENCES Capacity(name)
                                              ON DELETE CASCADE);

               INSERT INTO ValueType(name)
               VALUES ("Float"), ("Int"), ("String"), ("Bool");

               INSERT INTO ItemType(name)
               VALUES ("Equipment"), ("Utilitary");"""
                                   
def initDatabase(path, reinit=True):
    connection = sql.connect(path)
    if reinit:
        cursor     = connection.cursor()
        script = sqlInitDB
        script = script + """INSERT INTO EquipmentClass(name)
                             VALUES """

        for c in armoryClass:
            script = script + "(\"" + c + "\"), "

        if len(armoryClass) > 0:
            script = script[0:-2] + ";"
        connection.cursor().executescript(script)

    return connection

def recreateDatabase(bestiaryTab, armoryTab, handlePower, connection):
    saveCapacity(handlePower, connection)
    saveBestiaryDatas(bestiaryTab, connection)
    saveEquipmentData(armoryTab, connection)
    saveEquipmentCapacityData(armoryTab, connection)

    connection.commit()

def saveDatabase(connection):
    connection.commit()

def saveBestiaryDatas(bestiaryTab, connection):
    script = """INSERT INTO BestiaryType(name)
                VALUES """

    typeModel = bestiaryTab.typeWidget.get_model()
    typeIter  = typeModel.get_iter_first()
    miniScript = None
    
    while typeIter != None:
        miniScript = "(\"" + typeModel[typeIter][0] + "\"), "
        script = script + miniScript
        typeIter = typeModel.iter_next(typeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        connection.cursor().executescript(script)

    script = "INSERT INTO Bestiary(" + str.join(', ', [x.replace(" ", "") for x in bestiaryModel]) +")VALUES "

    bestiaryStore = bestiaryTab.store
    storeIter     = bestiaryTab.store.get_iter_first()
    miniScript = None
    while storeIter != None:
        miniScript = "("
        for i in range(len(bestiaryModel)):
            miniScript = miniScript + "\"" + str(bestiaryStore[storeIter][i]) + "\", "
        script = script + miniScript[0:-2] + "), "
        storeIter = bestiaryStore.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
        connection.cursor().executescript(script)

def saveEquipmentData(armoryTab, connection):
    model       = armoryTab.store
    treeIter    = armoryTab.store.get_iter_first()

    script = """INSERT INTO EquipmentType(name)
                VALUES """

    typeModel = armoryTab.typeWidget.get_model()
    typeIter  = typeModel.get_iter_first()
    miniScript = None

    while typeIter != None:
        miniScript = "(\""+typeModel[typeIter][0]+"\"), "
        script     = script + miniScript
        typeIter   = typeModel.iter_next(typeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
        connection.cursor().executescript(script)

    script = "INSERT INTO Equipment(" + str.join(', ', [x.replace(" ", "") for x in armoryModel]) + ") VALUES "

    model = armoryTab.store
    storeIter = model.get_iter_first()
    idIndex = armoryModel.index("ID")

    miniScript = None
    while storeIter != None:
        connection.cursor().executescript("INSERT INTO Item(id, type) VALUES ("+str(model[storeIter][idIndex])+", \"Equipment\");")
        miniScript = "("
        for i in range(len(armoryModel)):
            miniScript = miniScript + "\"" + str(model[storeIter][i]) + "\", "
        script = script + miniScript[0:-2] + "), "
        storeIter = model.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2]
        script = script.replace("\"\"", "NULL")
        connection.cursor().executescript(script)

def saveEquipmentCapacityData(armoryTab, connection):
    script = "INSERT INTO EquipmentCapacity(id, type, value) VALUES "
    miniScript = None
    for key, createPower in armoryTab.powerDict.items():
        iterPower = createPower.store.get_iter_first()
        while iterPower != None:
            miniScript = "(" + str(key) + ', '
            for i in range(2):
                miniScript = miniScript + "\"" + str(createPower.store[iterPower][i]) + "\", "
            script = script + miniScript[0:-2] + "), "
            iterPower = createPower.store.iter_next(iterPower)

    if miniScript != None:
        script = script[0:-2] + ";"
        connection.cursor().executescript(script)

def saveCapacity(handlePower, connection):
    script = """INSERT INTO Capacity(name, isGlobal, type, value, description)
              VALUES """

    store = handlePower.store
    storeIter = store.get_iter_first()
    miniScript = None

    while storeIter != None:
        miniScript = "(\"" + handlePower.store[storeIter][0] + "\",  " + str(int(handlePower.store[storeIter][1])) + ", \"" + handlePower.store[storeIter][2] +  "\", "

        if handlePower.store[storeIter][2] == "Int":
            miniScript = miniScript + str(int(handlePower.store[storeIter][3]))

        elif handlePower.store[storeIter][2] == "Float":
            miniScript = miniScript + str(float(handlePower.store[storeIter][3]))

        elif handlePower.store[storeIter][2] == "String":
            miniScript = miniScript + "\"" + handlePower.store[storeIter][3] + "\""

        elif handlePower.store[storeIter][2] == "Bool":
            miniScript = miniScript + str(int(handlePower.store[storeIter][3] != 0))

        desc = handlePower.store[storeIter][4] 
        script = script + miniScript + ", \""+ desc +"\"), "
        storeIter = store.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
        connection.cursor().executescript(script)

def loadDatas(bestiaryTab, armoryTab, handlePower, path):
    connection = sql.connect(path)
    loadCapacity(handlePower, connection)
    loadBestiary(bestiaryTab, connection)
    loadEquipment(armoryTab, connection)
    loadEquipmentCapacity(armoryTab, connection)

    cursor = connection.cursor().execute("SELECT * FROM SQLITE_SEQUENCE WHERE name = \"Bestiary\" OR name = \"Equipment\"");
    for row in cursor:
        if row[0] == "Bestiary":
            bestiaryTab.entryID = row[1]
        elif row[0] == "Equipment":
            armoryTab.entryID = row[1]

    return connection

def loadBestiary(bestiaryTab, connection):
    cursor  = connection.execute("SELECT * FROM Bestiary")
    for row in cursor:
        #!= 3 for the model statement
        l = [row[x] for x in range(len(row)) if x != 3]
        replaceNone(l)
        typeIndex = bestiaryModel.index("Type")
        bestiaryTab.store.append(l)
        addTextInComboBoxText(bestiaryTab.typeWidget, row[typeIndex] if row[typeIndex] != None else "")

def loadEquipment(armoryTab, connection):
    cursor = connection.execute("SELECT * FROM Equipment")
    for row in cursor:
        l = [row[x] for x in range(len(row)) if x != 4]
        replaceNone(l)
        armoryTab.appendStore(l)

def loadCapacity(handlePower, connection):
    cursor = connection.execute("SELECT * FROM Capacity")
    for row in cursor:
        l = [row[0], bool(row[1]), row[2], str(row[3]), row[4]]
        replaceNone(l)
        handlePower.store.append(l)

def loadEquipmentCapacity(armoryTab, connection):
    cursor = connection.execute("SELECT * FROM EquipmentCapacity")
    for row in cursor:
        armoryTab.powerDict[row[0]].store.append([str(row[x]) for x in range(1, len(row))])

def setDatabaseEntry(connection, t, kwargs):
    script = None

    if t == "BESTIARY_TYPE":
        script = """UPDATE BestiaryType
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "name"]) +\
                   "WHERE name=\'" + kwargs["name"] + "\';"
    elif t == "BESTIARY":
        script = """UPDATE Bestiary
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   "WHERE id=\'" + kwargs["id"] + "\';" 

    elif t == "CAPACITY":
        script = """UPDATE Capacity
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "name"]) +\
                   "WHERE name=\'" + kwargs["name"] + "\';" 

    elif t == "EQUIPMENT_CLASS":
        script = """UPDATE EquipmentClass
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "name"]) +\
                   "WHERE name=\'" + kwargs["name"] + "\';" 

    elif t == "ITEM":
        script = """UPDATE Item
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   "WHERE id=\'" + kwargs["id"] + "\';" 

    elif t == "EQUIPMENT_TYPE":
        script = """UPDATE EquipmentType
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "name"]) +\
                   "WHERE name=\'" + kwargs["name"] + "\';" 

    elif t == "EQUIPMENT":
        script = """UPDATE Equipment
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   "WHERE id=\'" + kwargs["id"] + "\';" 

    elif t == "EQUIPMENT_CAPACITY":
        script = """UPDATE EquipmentCapacity
                    SET """ + str.join(', ', [n + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   "WHERE id=\'" + kwargs["id"] + "\';" 

    if script != None:
        print(script)
        script = script.replace("\'\'", "NULL")
        connection.cursor().executescript(script)

def addDatabaseEntry(connection, t, values):
    script = None

    if t == "BESTIARY_TYPE":
        script = """INSERT INTO BestiaryType(name)
                    VALUES (\'""" + values[0] + "\');"

    elif t == "BESTIARY":
        script = """INSERT INTO Bestiary(id, type, name, pv, mp, ad, ap, pr, mr, size, weight, speed, attackSpeed, description) VALUES (\'""" + str.join('\', \'', [x.replace(" ", "") for x in values]) + "\');"

    elif t == "CAPACITY":
        script = """INSERT INTO Capacity(name, isGlobal, type, value, description)
                    VALUES (\'""" + values[0] + "\', \'" + str(int(values[1])) + "\', \'" + values[2] +  "\', \'"

        if values[2] == "Int":
            script = script + str(int(values[3]))
        elif values[2] == "Float":
            script = script + str(float(values[3]))
        elif values[2] == "String":
            script = script + values[3]
        elif values[2] == "Bool":
            script = script + str(int(values[3] != 0))
        script = script + "\', \'" + values[4] + "\');"

    elif t == "ITEM":
        script = "INSERT INTO Item(id, type) VALUES (\'"+values[0]+"\', \'Equipment\');"

    elif t == "EQUIPMENT_CLASS":
        script = """INSERT INTO EquipmentClass(name)
                    VALUES (\'""" + values[0] + "\');"

    elif t == "EQUIPMENT_TYPE":
        script = """INSERT INTO EquipmentType(name)
                    VALUES (\'""" + values[0] + "\');"

    elif t == "EQUIPMENT":
        script = """INSERT INTO Equipment(id, class, type, name, pv, mp, ad, ap, pr, mr, weight, speed, attackSpeed, description)
                   VALUES (\'""" + str.join('\', \'', [x.replace(" ", "") for x in values]) + "\');"

    elif t == "EQUIPMENT_CAPACITY":
        script = "INSERT INTO EquipmentCapacity(id, type, value) VALUES (\'" + str.join('\', \'', [x.replace(" ", "") for x in values]) + "\');"

    if script != None:
        script = script.replace("\'\'", "NULL")
        connection.cursor().executescript(script)
        print(script)

def deleteDatabaseEntry(connection, t, key):
    script = None
    if t == "BESTIARY_TYPE":
        script = "DELETE FROM BestiaryType      WHERE name = \'" + key + "\';"
    elif t == "BESTIARY":
        script = "DELETE FROM Bestiary          WHERE id = \'" + key + "\';"
    elif t == "CAPACITY":
        script = "DELETE FROM Capacity          WHERE name = \'" + key + "\';"
    elif t == "EQUIPMENT_CLASS":
        script = "DELETE FROM EquipmentClass    WHERE name = \'" + key + "\';"
    elif t == "ITEM":
        script = "DELETE FROM Item              WHERE id = \'" + key + "\';"
    elif t == "EQUIPMENT_TYPE":
        script = "DELETE FROM EquipmentType     WHERE name = \'" + key + "\';"
    elif t == "EQUIPMENT":
        script = "DELETE FROM Equipment         WHERE id = \'" + key + "\';"
    elif t == "EQUIPMENT_CAPACITY":
        script = "DELETE FROM EquipmentCapacity WHERE id = \'" + key + "\';"
