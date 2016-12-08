databaseWindow = None

classModel = [("Class Name", str),\
              ("Name", str)]

unitModel = [("ID", int),\
             ("Type Name", str),\
             ("Name", str),\
             ("Winged", bool),\
             ("Level", int),\
             ("Price", int),\
             ("Occupation", int),\
             ("PV", int),\
             ("MP", int),\
             ("AD", int),\
             ("AP", int),\
             ("PR", int),\
             ("MR", int),\
             ("Moving", int),\
             ("Attack Speed", float),\
             ("Move Stats", float),\
             ("Description", str)]

itemModel = ["ID",
             "Name",
             "Description"]

animModel = [("Unit Name", str, "unitName"),\
             ("Animation Name", str, "name"),\
             ("Type", str, "type"),\
             ("Image Path", str, "modelPath")]

staticModel = ["orientation", "x", "y", "sizeX", "sizeY", "padX", "padY", "n", "nX"]

mapModel = [("Name", str, "name"),\
            ("Map Path", str, "path"),\
            ("Minimap Path", str, "miniPath")]
