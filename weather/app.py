#!/usr/bin/env python3
"""
Weather DB: Plots hourly readings for weather data points (temp, humidity, etc).
"""
import csv
import json
import time

import weather.classes.app_config as cfg
import weather.classes.logger as log
import weather.db.model as mdl
import weather.db.weatherdb as db
import weather.model.config_keys as cfgKeys
import weather.model.service_error as svc

from weather.util.utils import LoadTextFile, LogError, LogWarn, LogInfo

testMode = False

"""
def getMeasurements(config: cfg.ApplicationConfig, conn, stationCode: str, year: int, month:int, hours: tuple):
    global actionSwitch

    updateList, serr = rbacdm.GetPolicyUpdates(config, conn)
    updateMap = {}
    catalogGroups = {}

    if serr.isError():
        serr = reportError(config, "...error querying db: serr = [{}]", serr)
    else:
        logInfo(f"...got {len(updateList)} policy update rows from RBAC")

        for rbacUpdate in updateList:
            catalogGroups = updateCatalogUsers(catalogGroups, rbacUpdate.getAsList(db.KEY_CATALOG), rbacUpdate.getAsList(db.KEY_GROUP), rbacUpdate.getAsList(db.KEY_USER))
            policyUpdate: db.RangerPolicy = ToRangerPolicy(config.ValueOf(cfgKeys.KEY_POLICY_MANAGER_SERVICE), rbacUpdate)

            rpd = updateMap.get(policyUpdate.getField('name'))
            action = actionSwitch.get(rbacUpdate.get(db.KEY_ACTION).upper())
            if rpd:
                rpd['policy'].mergeWith(policyUpdate)
                rpd['dbkeys'].append(rbacUpdate.get(db.KEY_ID))
                if rpd['valid']:
                    rpd['valid'] = (rpd['action'] == action)
            else:
                rpd = {
                    'policy': policyUpdate,
                    'action': action,
                    'dbkeys': [rbacUpdate.get(db.KEY_ID)],
                    'valid': True
                }
                updateMap[policyUpdate.getField('name')] = rpd

        if len(updateList) > 0:
            logInfo(f"...converted RBAC rows to {len(updateMap)} Ranger policies...")

    return (updateMap, catalogGroups, serr)
# end def: getMeasurements
"""

def get_station(config: cfg.ApplicationConfig, conn):
    serr = svc.NoError
    station = None

    if conn:
        try:
            stationCode = config.ValueOf(cfgKeys.KEY_CLIENT_PARAMS)
            station, serr = db.get_station(conn, stationCode)
            if not serr.isError():
                print(station.toJson())
        except Exception as err:
            serr = svc.DbQueryError.withCause(err)

    return serr
# end def: get_station

def update_weatherdb(config: cfg.ApplicationConfig, conn):
    serr = svc.NoError

    file = config.ValueOf(cfgKeys.KEY_CLIENT_INPUT)
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        fields_list = next(reader)
        for row in reader:
            station = db.Station(row[0], row[1], float(row[2]), float(row[3]), float(row[4]))
            try:
                db.upsert_station(conn, station)
            except Exception as err:
                serr = svc.DbQueryError.withCause(err)

            """
            measurement = db.Measurement(year, (0, stationCode, 0, f"{month:02d}-01T{hour:02d}:00:00", year, measurement))

            try:
                db.AddMeasurement(conn, measurement)
            except Exception as err:
                serr = svc.DbQueryError.withCause(err)
            """

    return serr
# end def: update_weatherdb

def read_input(config):
    serr = svc.NoError
    data = ""

    try:
        data = LoadTextFile(config.ValueOf(cfgKeys.KEY_CLIENT_INPUT))
    except Exception as err:
        serr = svc.ClientInputError.withCause(err)

    return (data, serr)
# end def: readInput

def execute(config: cfg.ApplicationConfig):
    serr = svc.NoError
    cmd = config.ValueOf(cfgKeys.KEY_CLIENT_COMMAND)

    if config.AssignedValue(cfgKeys.KEY_CLIENT_INPUT) or config.AssignedValue(cfgKeys.KEY_CLIENT_PARAMS):
        conn, serr = db.connect(config)

        if not serr.isError():
            if cmd == 'UpdateDatabase':
                serr = update_weatherdb(config, conn)
            elif cmd == 'GetStation':
                serr = get_station(config, conn)

        db.close(conn)

    return serr
# end def: execute

def main():
    global testMode

    serr = svc.NoError

    # Initialize the logger
    log.Logger()

    config = cfg.ApplicationConfig()
    if config.AssignedValue(cfgKeys.KEY_TEST_MODE):
        testMode = (config.ValueOf(cfgKeys.KEY_TEST_MODE).lower() == "true")

    if config.AssignedValue(cfgKeys.KEY_CLIENT_COMMAND):
        switch = {
            "GetMeasurements": True,
            "GetStation": True,
            "UpdateDatabase": True
        }
        doExec = switch.get(config.ValueOf(cfgKeys.KEY_CLIENT_COMMAND), False)
        if not doExec:
            logError("Unknown command specified", None)
            exit()

        if config.AssignedValue(cfgKeys.KEY_CLIENT_INPUT):
            logInfo("Starting in command mode {} with input {}...".format(
                config.ValueOf(cfgKeys.KEY_CLIENT_COMMAND),
                config.ValueOf(cfgKeys.KEY_CLIENT_INPUT)))
        elif config.AssignedValue(cfgKeys.KEY_CLIENT_PARAMS):
            logInfo("Starting in command mode {} with params {}...".format(
                config.ValueOf(cfgKeys.KEY_CLIENT_COMMAND),
                config.ValueOf(cfgKeys.KEY_CLIENT_PARAMS)))
        else:
            logInfo("Starting in command mode {}...".format(
                config.ValueOf(cfgKeys.KEY_CLIENT_COMMAND)))

        serr = execute(config)

    if serr.isError():
        logInfo(f"Exiting, with error = {serr.toString()}.")
    else:
        logInfo(f"Done.")
# end def: main

def logInfo(message):
    LogInfo("weather-plotter", message)
# end def: logInfo

def logWarn(message, cause=None):
    LogWarn("weather-plotter", message, cause)
# end def: logWarn

def logError(message, cause=None):
    LogError("weather-plotter", message, cause)
# end def: logError

def mergeLists(list1, list2):
    for item in list2:
        if item not in list1:
            list1.append(item)

    return list1
# end def: mergeLists

def reportError(config = cfg.ApplicationConfig, mesgTmpl = str, serr = None):
    if serr:
        mesg = mesgTmpl.format(serr.toString())
    else:
        mesg = mesgTmpl
    logError(mesg)

    return serr
# end def: reportError

def traceIt(message):
    global testMode

    if testMode:
        logInfo(message)
# end def: traceIt

# Get the show on the road!
if __name__ == '__main__':
    main()
