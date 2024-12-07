import weather.db.model as model
import weather.model.config_keys as cfgKeys
import weather.model.service_error as svc
import weather.util.config as ini

from sqlalchemy import create_engine, text

from weather.classes.app_config import ApplicationConfig
from weather.util.utils import LogInfo

KEY_AUTO_COMMIT = "autoCommit"
KEY_AUTH_TYPE   = "authType"
KEY_DB_NAME     = "databaseName"
KEY_DB_URL      = "connectionUrl"
KEY_GET_MEASUREMENTS_STMT = "getMeasurements"
KEY_GET_STATION_STMT = "getStation"
KEY_ADD_STATION_STMT = "addStation"
KEY_UPDATE_STATION_STMT = "updateStation"
KEY_SET_UPDATED_STMT = "flagPolicyUpdated"
KEY_UPDATE_BY_KEY    = "flagPolicyByKey"

_dbConfig: ini.IniConfig = None
_dbProps = None
_dbEngine = None

def close(conn, cursor=None):
    if cursor:
        cursor.close()

    if conn:
        conn.close()
# end def: CloseDb

def connect(config: ApplicationConfig):
    """ Connect to the Weather database server """
    global _dbConfig, _dbEngine, _dbProps
    serr = svc.NoError
    conn = None
    connString = None

    if _dbConfig == None:
        if not config.AssignedValue(cfgKeys.KEY_WEATHERDB_HOST_IP):
            serr = svc.DbOpenError.withCause(Exception("Weather DB host not configured."))
        elif not config.AssignedValue(cfgKeys.KEY_WEATHERDB_PORT_NUM):
            serr = svc.DbOpenError.withCause(Exception("Weather DB port not configured."))
        elif not config.AssignedValue(cfgKeys.KEY_WEATHERDB_LOGIN):
            serr = svc.DbOpenError.withCause(Exception("Weather DB login name not configured."))
        elif not config.AssignedValue(cfgKeys.KEY_WEATHERDB_PASSWORD):
            serr = svc.DbOpenError.withCause(Exception("Weather DB password not configured."))
        elif not config.AssignedValue(cfgKeys.KEY_WEATHERDB_CONFIG):
            serr = svc.DbOpenError.withCause(Exception("Weather DB access config file not configured."))

        if not serr.isError():
            targetCfg = config.ValueOf(cfgKeys.KEY_WEATHERDB_CONFIG)

            secure = "no"
            if config.AssignedValue(cfgKeys.KEY_WEATHERDB_SSL_ENABLED):
                secure = config.ValueOf(cfgKeys.KEY_WEATHERDB_SSL_ENABLED)

            _dbConfig = ini.IniConfig("./config/db/{}.ini".format(targetCfg))
            _dbProps = {
                'host': config.ValueOf(cfgKeys.KEY_WEATHERDB_HOST_IP),
                'port': config.ValueOf(cfgKeys.KEY_WEATHERDB_PORT_NUM),
                'user': config.ValueOf(cfgKeys.KEY_WEATHERDB_LOGIN),
                'password': config.ValueOf(cfgKeys.KEY_WEATHERDB_PASSWORD),
                'database': _dbConfig.get_value(KEY_DB_NAME, 'Main'),
                'secure': secure,
                KEY_AUTH_TYPE: 'connString'
            }

            connString = _dbConfig.get_value(KEY_DB_URL, 'Main').format(**_dbProps)

            #traceIt(config, "DB config: {}".format(connString))

    if not serr.isError():
        try:
            if not _dbEngine:
                _dbEngine = create_engine(connString)

            conn = _dbEngine.connect()
        except Exception as err:
            serr = svc.DbOpenError.withCause(err)

    return (conn, serr)
# end def: ConnectDb

"""
def get_measurements(conn, stationCode: str, year: int, month:int, days: tuple = (-1), hours: tuple = (-1)):
    " "" Query and return the list of measurements "" "
    global _dbConfig
    serr = svc.NoError
    measurementList = []

    if conn:
        if days == (-1) and hours == (-1):
            try:
                results = conn.execute(text(_dbConfig.get_value(KEY_GET_MEASUREMENTS_STMT, 'Main').format(stationCode, year, f"{month:02d}")))

                for row in results:
                    model.Measurement(year, (row[0], stationCode, row[1], row[2], year, row[3]))

                    measurementList.append(model.MeasurementRow(row))
            except Exception as err:
                serr = svc.DbQueryError.withCause(err)
        elif hours == (-1):
            for day in days:
                try:
                    results = conn.execute(text(_dbConfig.get_value(KEY_GET_MEASUREMENTS_STMT, 'Main').format(stationCode, year, f"{month:02d}-{day:02d}")))

                    for row in results:
                        model.Measurement(year, (row[0], stationCode, row[1], row[2], year, row[3]))

                        measurementList.append(model.MeasurementRow(row))
                except Exception as err:
                    serr = svc.DbQueryError.withCause(err)
        else:
            for hour in hours:
                try:
                    results = conn.execute(text(_dbConfig.get_value(KEY_GET_MEASUREMENTS_STMT, 'Main').format(stationCode, year, f"{month:02d}-%T{hour:02d}")))

                    for row in results:
                        model.Measurement(year, (row[0], stationCode, row[1], row[2], year, row[3]))

                        measurementList.append(model.MeasurementRow(row))
                except Exception as err:
                    serr = svc.DbQueryError.withCause(err)



            for day in range(1, 32):

                hour = f"{month:02d}"
        if hours == (-1):
            hours = range(0, 24)
        for hour in hours:
            for day in range(1,32):
                hourstr = f"{month:02d}-{day:02d}T{hour:02d}:00:00"
                try:
                    results = conn.execute(text(_dbConfig.get_value(KEY_GET_MEASUREMENTS_STMT, 'Main').format(stationCode, year, hourstr)))

                    for row in results:
                        model.Measurement(year, (row[0], stationCode, row[1], hourstr, year, row[2]))
                        
                        measurementList.append(model.MeasurementRow(row))
                except Exception as err:
                    serr = svc.DbQueryError.withCause(err)
        try:
            results = conn.execute(text(_dbConfig.get_value(KEY_GET_MEASUREMENTS_STMT, 'Main')))
            
            for row in results:
                updateList.append(model.PolicyRow(row))
        except Exception as err:
            serr = svc.DbQueryError.withCause(err)

    return (updateList, serr)
# end def: GetPolicyUpdates
"""

def get_station(conn, stationCode: str):
    """ Query and return the specified station """
    global _dbConfig
    serr = svc.NoError
    station = None

    if conn:
        try:
            results = conn.execute(text(_dbConfig.get_value(KEY_GET_STATION_STMT, 'Main').format(stationCode)))

            if results:
                row = results.fetchone()
                station = model.Station(row)
        except Exception as err:
            serr = svc.DbQueryError.withCause(err)

    return (station, serr)
# end def: get_station

def upsert_station(config: ApplicationConfig, conn, station: model.Station):
    """ Flag the specified policy as being successfully processed """
    global _dbConfig
    serr = svc.NoError

    if conn:
        try:
            _station, serr = get_station(conn, station.get(model.KEY_CODE))
            if serr.isError():
                return serr
            elif _station == None:
                stmt = _dbConfig.get_value(KEY_ADD_STATION_STMT, 'Main').format(station.get(model.KEY_CODE), station.get(model.KEY_STATION_NAME), station.get(model.KEY_LATITUDE), station.get(model.KEY_LONGITUDE), station.get(model.KEY_ELEVATION))
            elif _station.toString() != station.toString():
                stmt = _dbConfig.get_value(KEY_UPDATE_STATION_STMT, 'Main').format(station.get(model.KEY_STATION_NAME), station.get(model.KEY_LATITUDE), station.get(model.KEY_LONGITUDE), station.get(model.KEY_ELEVATION), station.get(model.KEY_CODE))

            conn.execute(text(stmt))

            if _dbConfig.get_value(KEY_AUTO_COMMIT, 'Main') and (_dbConfig.get_value(KEY_AUTO_COMMIT, 'Main').lower() == "false"):
                conn.commit()
        except Exception as err:
            serr = svc.DbUpdateError.withCause(err)

    return serr
# end def: upsert_station

def logInfo(message):
    LogInfo("rbacdm", message)
# end def: logIt

def traceIt(config: ApplicationConfig, message):
    testMode = False
    if config.AssignedValue(cfgKeys.KEY_TEST_MODE):
        testMode = (config.ValueOf(cfgKeys.KEY_TEST_MODE).lower() == "true")
    
    if testMode:
        logInfo(message)
# end def: traceIt
