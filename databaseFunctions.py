from io import StringIO
from UnitTab import UnitTab
from globalVar import *
from functions import *

import sqlite3 as sql

sqlInitDB = """
               CREATE TABLE Class(name VARCHAR(32) PRIMARY KEY);

               CREATE TABLE Type(className VARCHAR(32),
                                 name VARCHAR(32) PRIMARY KEY,
                                 FOREIGN KEY(className) REFERENCES Class(name));

               CREATE TABLE ValueType(name VARCHAR(32) PRIMARY KEY);

               CREATE TABLE Unit(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                      typeName   VARCHAR(32),
                                      name        VARCHAR(32),
                                      winged      BOOL,
                                      level       INTEGER,
                                      price       INTEGER,
                                      occupation  INTEGER,
                                      modelPath   TEXT,
                                      pv          INTEGER,
                                      mp          INTEGER,
                                      ad          INTEGER,
                                      ap          INTEGER,
                                      pr          INTEGER,
                                      mr          INTEGER,
                                      moving      INTEGER,
                                      attackSpeed FLOAT,
                                      moveStats   FLOAT,
                                      description TEXT,
                                      FOREIGN KEY(typeName) REFERENCES Type(name));

               CREATE TABLE Capacity(name VARCHAR(32) PRIMARY KEY,
                                     isGlobal TINYINT NOT NULL,
                                     type  VARCHAR(32),
                                     value BLOB,
                                     description TEXT,
                                     FOREIGN KEY(type) REFERENCES ValueType(name));

               CREATE TABLE Capacity_Unit(idUnit INTEGER,
                                          capacityName VARCHAR(32),
                                          FOREIGN KEY(idUnit) REFERENCES Unit(id),
                                          FOREIGN KEY(capacityName) REFERENCES Capacity(name));

               CREATE TABLE ItemType(name VARCHAR(32) PRIMARY KEY);
            
               CREATE TABLE Item(id INTEGER PRIMARY KEY,
                                  type VARCHAR(32) NOT NULL,
                                  FOREIGN KEY(type) REFERENCES ItemType(name));

               INSERT INTO ValueType(name)
               VALUES ("Float"), ("Int"), ("String"), ("Bool");"""
                                   
def initDatabase(path, reinit=True):
    connection = sql.connect(path)
    if reinit:
        cursor = connection.cursor()
        script = sqlInitDB
        connection.cursor().executescript(script)

    return connection

def recreateDatabase(classTab, unitTab, handlePower, connection):
    print("recreate class")
    saveClass(classTab, connection)
    print("recreate type")
    saveType(classTab, connection)
    saveCapacity(handlePower, connection)
    saveUnitDatas(unitTab, connection)

    connection.commit()

def saveDatabase(connection):
    connection.commit()

def saveClass(classTab, connection):
    script = "INSERT INTO Class(name) VALUES "
    listClass = []
    classStore = classTab.store
    storeIter = classTab.store.get_iter_first()
    miniScript = None

    while storeIter != None:
        if classStore[storeIter][0] not in listClass:
            listClass.append(classStore[storeIter][0])
        else:
            storeIter = classStore.iter_next(storeIter)
            continue

        miniScript = "("
        miniScript = miniScript + "\"" + str(classStore[storeIter][0]) + "\""
        script = script + miniScript + "), "
        storeIter = classStore.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
        print(script)
        connection.cursor().executescript(script)

def saveType(classTab, connection):
    classStore = classTab.store
    storeIter = classTab.store.get_iter_first()
    childIter = None

    script = "INSERT INTO Type(" + str.join(', ', [x[0].replace(" ", "") for x in classModel]) +") VALUES "

    miniScript = None

    while storeIter != None:
        childIter = classStore.iter_children(storeIter)

        while childIter != None:
            miniScript = "("
            miniScript = miniScript + "\"" + classStore[storeIter][0] + '\", \"' + classStore[childIter][0] + "\", "
            script = script + miniScript[0:-2] + "), "
            childIter = classStore.iter_next(childIter)
        storeIter = classStore.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
        print(script)
        connection.cursor().executescript(script)

def saveUnitDatas(unitTab, connection):
    script = "INSERT INTO Unit(" + str.join(', ', [x[0].replace(" ", "") for x in unitModel]) +")VALUES "

    unitStore = unitTab.store
    storeIter  = unitTab.store.get_iter_first()
    miniScript = None
    while storeIter != None:
        miniScript = "("
        for i in range(len(unitModel)):
            miniScript = miniScript + "\"" + str(unitStore[storeIter][i]) + "\", "
        script = script + miniScript[0:-2] + "), "
        storeIter = unitStore.iter_next(storeIter)

    if miniScript != None:
        script = script[0:-2] + ";"
        script = script.replace("\"\"", "NULL")
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

def loadDatas(classTab, unitTab, handlePower, path):
    connection = sql.connect(path)
    loadClass(classTab, connection)
    loadCapacity(handlePower, connection)
    loadUnit(unitTab, connection)

    cursor = connection.cursor().execute("SELECT * FROM SQLITE_SEQUENCE WHERE name = \'Unit\'");
    for row in cursor:
        if row[0] == "Unit":
            unitTab.idEntry = int(row[1]) + 1

    return connection

def loadClass(classTab, connection):
    cursor = connection.execute("SELECT * FROM Type")
    for row in cursor:
        classTab.loadEntry(row, False)

def loadUnit(unitTab, connection):
    cursor  = connection.execute("SELECT * FROM Unit")
    modelIndex = 7
    for row in cursor:
        l = [row[x] for x in range(len(row)) if x != modelIndex]
        replaceNone(l)
        typeIndex = unitModel.index(("Type Name", str))
        unitTab.store.append(l)

def loadCapacity(handlePower, connection):
    cursor = connection.execute("SELECT * FROM Capacity")
    for row in cursor:
        l = [row[0], bool(row[1]), row[2], str(row[3]), row[4]]
        replaceNone(l)
        handlePower.store.append(l)


def setDatabaseEntry(connection, t, key, entry, value):
    script = None

    if t == "UNIT":
        script = """UPDATE Unit
                    SET \'""" + entry.replace(" ", "") + "\' = " + "\"" + str(value) + "\" "\
                   "WHERE id=\'" + key + "\';" 

    elif t == "CAPACITY":
        script = """UPDATE Capacity
                    SET """ + entry.replace(" ", "") + " = " + str(value) +\
                   "WHERE name=\'" + key + "\';" 

    elif t == "ITEM":
        script = """UPDATE Item
                    SET """ + entry.replace(" ", "") + " = " + str(value) +\
                   "WHERE id=\'" + key + "\';" 

    if script != None:
        print(script)
        script = script.replace("\'\'", "NULL")
        connection.cursor().executescript(script)


def setDatabaseEntryKwargs(connection, t, kwargs):
    script = None

    if t == "UNIT":
        script = """UPDATE Unit
                    SET """ + str.join(', ', ["\"" + n.replace(" ", "") + "\" = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   " WHERE id=\'" + kwargs["id"] + "\';" 

    elif t == "CAPACITY":
        script = """UPDATE Capacity
                    SET """ + str.join(', ', [n.replace(" ", "") + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "name"]) +\
                   " WHERE name=\'" + kwargs["name"] + "\';" 

    elif t == "ITEM":
        script = """UPDATE Item
                    SET """ + str.join(', ', [n.replace(" ", "") + " = \'" + v + "\'" for (n, v) in kwargs.items() if n != "id"]) +\
                   " WHERE id=\'" + kwargs["id"] + "\';" 

    if script != None:
        print(script)
        script = script.replace("\'\'", "NULL")
        connection.cursor().executescript(script)

def addDatabaseEntry(connection, t, values):
    script = None

    if t == "UNIT":
        script = """INSERT INTO Unit(id, typeName, name, winged, level, price, occupation, pv, mp, ad, ap, pr, mr, moving, attackSpeed, moveStats, description) VALUES (""" + str.join(', ', ["\"" + x + "\"" for x in values]) + ");"

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

    elif t == "CLASS":
        script = """INSERT INTO Class(name) VALUES (\'""" + str(values[0]) + "\');"

    elif t == "TYPE":
        script = """INSERT INTO Type(className, name) VALUES (\'""" + str.join('\', \'', [x for x in values]) + "\');"

    elif t == "ITEM":
        script = "INSERT INTO Item(id, type) VALUES (\'"+values[0]+"\', \'Equipment\');"

    if script != None:
        script = script.replace("\'\'", "NULL")
        print(script)
        connection.cursor().executescript(script)

def deleteDatabaseEntry(connection, t, key):
    script = None
    if t == "UNIT":
        script = "DELETE FROM Unit          WHERE id = \'" + key + "\';"
    elif t == "CAPACITY":
        script = "DELETE FROM Capacity          WHERE name = \'" + key + "\';"
    elif t == "ITEM":
        script = "DELETE FROM Item              WHERE id = \'" + key + "\';"
