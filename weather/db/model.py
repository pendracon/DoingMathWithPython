import json
from decimal import Decimal

KEY_CODE = "code"
KEY_DATA_TYPE_ID = "data_type_id"
KEY_DESC = "descr"
KEY_HOUR = "hour"
KEY_ID = "id"
KEY_LATITUDE = "latitude"
KEY_LONGITUDE = "longitude"
KEY_ELEVATION = "elevation"
KEY_MEASUREMENT = "measurement"
KEY_STATION_ID = "station_code"
KEY_STATION_NAME = "station_name"
KEY_YEAR = "year"

class DataType():
    def __init__(self, id: str, desc: str):
        self.schema = {
            KEY_DATA_TYPE_ID: str,
            KEY_DESC: str
        }

        self.schema[KEY_DATA_TYPE_ID] = str(id)
        self.schema[KEY_DESC] = str(desc)
    # end def: __init__

    def get(self, key: str) -> str:
        if key in self.schema:
            return self.schema[key]
        else:
            return None
    # end def: get

    def asDict(self) -> dict:
        return self.schema
    # end def: asDict

    def toString(self) -> str:
        return f"{self.schema}"
    # end def: toString

    def toJson(self) -> str:
        return json.dumps(self.schema)
    # end def: toJson
# end class: DataType

class Station():
    def __init__(self, row_t: tuple):
        self.schema = {
            KEY_CODE: str,
            KEY_STATION_NAME: str,
            KEY_LATITUDE: float,
            KEY_LONGITUDE: float,
            KEY_ELEVATION: float
        }

        self.schema[KEY_CODE] = str(row_t[0])
        self.schema[KEY_STATION_NAME] = str(row_t[1])
        self.schema[KEY_LATITUDE] = float(row_t[2])
        self.schema[KEY_LONGITUDE] = float(row_t[3])
        self.schema[KEY_ELEVATION] = float(row_t[4])
    # end def: __init__

    def get(self, key: str) -> str:
        if key in self.schema:
            return self.schema[key]
        else:
            return None
    # end def: get

    def asDict(self) -> dict:
        return self.schema
    # end def: asDict

    def toString(self) -> str:
        return f"{self.schema}"
    # end def: toString

    def toJson(self, prettyPrint: bool = False) -> str:
        if prettyPrint:
            return json.dumps(self.schema, indent=4)
        else:
            return json.dumps(self.schema)
    # end def: toJson
# end class: Station

class Measurement():
    def __init__(self, year:int, row_t: tuple):
        self.schema = {
            KEY_ID: int,
            KEY_STATION_ID: str,
            KEY_YEAR: int,
            KEY_HOUR: str,
            KEY_DATA_TYPE_ID: str,
            KEY_MEASUREMENT: float
        }

        self.schema[KEY_ID] = int(row_t[0])
        self.schema[KEY_STATION_ID] = str(row_t[1])
        self.schema[KEY_YEAR] = int(year)
        self.schema[KEY_HOUR] = str(row_t[3])
        self.schema[KEY_DATA_TYPE_ID] = str(row_t[4])
        self.schema[KEY_MEASUREMENT] = float(row_t[5])
    # end def: __init__

    def get(self, key: str) -> str:
        if key in self.schema:
            return self.schema[key]
        else:
            return None
    # end def: get

    def asDict(self) -> dict:
        return self.schema
    # end def: asDict

    def toString(self) -> str:
        return f"{self.schema}"
    # end def: toString

    def toJson(self) -> str:
        return json.dumps(self.schema)
    # end def: toJson
# end class: Measurement
