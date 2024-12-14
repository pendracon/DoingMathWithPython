import weather.db.model as mdl
import weather.model.config_keys as cfgKeys
import weather.model.service_error as svc
import weather.util.config as ini

from sqlalchemy import create_engine, text

from weather.classes.app_config import ApplicationConfig
from weather.util.utils import LogInfo

KEY_AUTO_COMMIT = "autoCommit"
KEY_DB_NAME     = "databaseName"
KEY_DB_URL      = "connectionUrl"

# data types statement keys - column precedence: data_type_id, descr[iption]
KEY_GET_DATATYPE_STMT = "getDataType"

# measurements statement keys - column precedence: station_code, year, hour, data_type_id, measurement
KEY_GET_HOURLY_MEASUREMENTS_STMT = "getMeasurements"
KEY_GET_MEASUREMENTS_BY_DATE_STMT = "getMeasurementsByDate"
KEY_GET_MEASUREMENTS_BY_TYPE_STMT = "getMeasurementsByType"
KEY_ADD_MEASUREMENT_STMT = "addMeasurement"
KEY_UPDATE_MEASUREMENT_STMT = "updateMeasurement"

# stations statement keys - column precedence: code, station_name, latitude, longitude, elevation
KEY_GET_STATION_STMT = "getStation"
KEY_ADD_STATION_STMT = "addStation"
KEY_UPDATE_STATION_STMT = "updateStation"

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
                'secure': secure
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

def execute_statement(config: ApplicationConfig, conn, statement: str = ''):
    """ Query and return the specified station """
    serr = svc.NoError
    stmt_results = []

    if conn:
        try:
            #print("Executing statement: {}".format(statement))
            results = conn.execute(text(statement))

            if results.returns_rows:
                #print(results)
                for row in results:
                    stmt_results.append(row)
        except Exception as err:
            traceIt(config, "Error in execute_statement: {0}\nStatement: {1}".format(err, statement))
            serr = svc.DbQueryError.withCause(err)

    return (stmt_results, serr)
# end def: execute_statement

def get_datatype(config: ApplicationConfig, conn, dataType: str):
    """ Query and return information about the specified weather data type """
    global _dbConfig
    data_type = None

    results, serr = execute_statement(config, conn, _dbConfig.get_value(KEY_GET_DATATYPE_STMT, 'Main').format(dataType))

    if len(results) > 0:
        row = results[0]
        data_type = mdl.DataType(row[0], row[1])

    return (data_type, serr)
# end def: get_datatype

def get_measurement(config: ApplicationConfig, conn, stationId: str, year: int, hour: str, dataTypeId: str):
    """ Query and return the specified measurement """
    return get_hourly_measurements(config, conn, stationId, year, hour, hour, dataTypeId)
# end def: get_measurement

def get_hourly_measurements(config: ApplicationConfig, conn, station_id: str, year: int, hour_start: str, hour_end: str, data_type_id: str):
    """ Query and return the list of measurements """
    global _dbConfig
    serr = svc.NoError
    measurements = []

    stmt = _dbConfig.get_value(KEY_GET_MEASUREMENTS_BY_TYPE_STMT, 'Main').format(station_id, year, hour_start, hour_end, data_type_id)
    results, serr = execute_statement(config, conn, stmt)

    if not serr.isError():
        for row in results:
            #print("row: {}".format(row))
            if len(row) > 0:
                measurements.append(mdl.Measurement(year, row))

    return (measurements, serr)
# end def: get_hourly_measurements

def get_station(config: ApplicationConfig, conn, stationCode: str):
    """ Query and return the specified station """
    global _dbConfig
    station = None

    results, serr = execute_statement(config, conn, _dbConfig.get_value(KEY_GET_STATION_STMT, 'Main').format(stationCode))

    if not serr.isError() and len(results) > 0:
        row = results[0]
        station = mdl.Station(row)

    return (station, serr)
# end def: get_station

def upsert_measurement(config: ApplicationConfig, conn, measurement: mdl.Measurement):
    """ Add or update the given measurement """
    global _dbConfig
    serr = svc.NoError

    stmt = None
    try:
        _measurements, serr = get_measurement(config, conn,
                                                measurement.get(mdl.KEY_STATION_ID),
                                                measurement.get(mdl.KEY_YEAR),
                                                measurement.get(mdl.KEY_HOUR),
                                                measurement.get(mdl.KEY_DATA_TYPE_ID))

        if serr.isError():
            pass
        elif len(_measurements) < 1:
            stmt = _dbConfig.get_value(KEY_ADD_MEASUREMENT_STMT, 'Main').format(
                                    measurement.get(mdl.KEY_STATION_ID),
                                    measurement.get(mdl.KEY_YEAR),
                                    measurement.get(mdl.KEY_HOUR),
                                    measurement.get(mdl.KEY_DATA_TYPE_ID),
                                    measurement.get(mdl.KEY_MEASUREMENT))

        elif len(_measurements) == 1:
            if _measurements[0].toString() != measurement.toString():
                stmt = _dbConfig.get_value(KEY_UPDATE_MEASUREMENT_STMT, 'Main').format(
                                        measurement.get(mdl.KEY_STATION_ID),
                                        measurement.get(mdl.KEY_YEAR),
                                        measurement.get(mdl.KEY_HOUR),
                                        measurement.get(mdl.KEY_DATA_TYPE_ID),
                                        measurement.get(mdl.KEY_MEASUREMENT),
                                        _measurements[0].get(mdl.KEY_ID))

        else:
            raise Exception("Multiple measurements found for station: {0}, year: {1}, hour: {2}, data type: {3}".format(
                                                measurement.get(mdl.KEY_STATION_ID),
                                                measurement.get(mdl.KEY_YEAR),
                                                measurement.get(mdl.KEY_HOUR),
                                                measurement.get(mdl.KEY_DATA_TYPE_ID)))

        if stmt:
            execute_statement(config, conn, stmt)

            if _dbConfig.get_value(KEY_AUTO_COMMIT, 'Main') and (_dbConfig.get_value(KEY_AUTO_COMMIT, 'Main').lower() == "false"):
                conn.commit()
    except Exception as err:
        traceIt(config, "Error in upsert_measurement: {0}\nStatement: {1}".format(err, stmt))
        serr = svc.DbUpdateError.withCause(err)

    return serr
# end def: upsert_measurement

def upsert_station(config: ApplicationConfig, conn, station: mdl.Station):
    """ Add or update the specified station """
    global _dbConfig
    serr = svc.NoError

    stmt = None
    try:
        _station, serr = get_station(config, conn, station.get(mdl.KEY_CODE))
        if serr.isError():
            pass
        elif _station == None:
            stmt = _dbConfig.get_value(KEY_ADD_STATION_STMT, 'Main').format(
                                    station.get(mdl.KEY_CODE),
                                    station.get(mdl.KEY_STATION_NAME),
                                    station.get(mdl.KEY_LATITUDE),
                                    station.get(mdl.KEY_LONGITUDE),
                                    station.get(mdl.KEY_ELEVATION))

        elif _station.toString() != station.toString():
            stmt = _dbConfig.get_value(KEY_UPDATE_STATION_STMT, 'Main').format(
                                    station.get(mdl.KEY_STATION_NAME),
                                    station.get(mdl.KEY_LATITUDE),
                                    station.get(mdl.KEY_LONGITUDE),
                                    station.get(mdl.KEY_ELEVATION),
                                    _station.get(mdl.KEY_CODE))

        if stmt:
            execute_statement(config, conn, stmt)

            if _dbConfig.get_value(KEY_AUTO_COMMIT, 'Main') and (_dbConfig.get_value(KEY_AUTO_COMMIT, 'Main').lower() == "false"):
                conn.commit()
    except Exception as err:
        traceIt(config, "Error in upsert_station: {0}\nStatement: {1}".format(err, stmt))
        serr = svc.DbUpdateError.withCause(err)

    return serr
# end def: upsert_station

def logInfo(message):
    LogInfo("weatherdb", message)
# end def: logIt

def traceIt(config: ApplicationConfig, message):
    testMode = False
    if config.AssignedValue(cfgKeys.KEY_TEST_MODE):
        testMode = (config.ValueOf(cfgKeys.KEY_TEST_MODE).lower() == "true")
    
    if testMode:
        logInfo(message)
# end def: traceIt
