from time import struct_time

import weather.classes.logger as log
from weather.model.service_error import DatetimeError, NoError

def LoadTextFile(filePath) -> str:
    textFile = open(filePath)

    content = ""
    for line in textFile.readlines():
        content = f"{content}{line}"

    return content
# end def: LoadTextFile

def ParseOptions(argSwitch, argSeparator, args):
    opts = {}

    v = []
    for idx in range(0, len(args)):
        if argSeparator == ' ':
            if idx % 2 == 1:
                opts[v[0]] = args[idx]
            else:
                v[0] = args[idx]
                opts[args[idx]] = ""
        elif argSeparator in args[idx]:
            if args[idx].startswith(argSwitch):
                v = args[idx][len(argSwitch):].split(argSeparator)
            else:
                v = args[idx].split(argSeparator)
            opts[v[0]] = v[1]
        else:
            # presume a flag switch
            if args[idx].startswith(argSwitch):
                opts[args[idx][len(argSwitch):]] = "true"

    return opts
# end def: ParseOptions

def StripDateStamp(datetime):
    return datetime.replace("-", "").replace(":", "").replace("T", "").replace("Z", "")
# end def: StripDateStamp

def ToDatetime(tstamp):
    serr = NoError
    datetime = None

    try:
        year = int(tstamp[0:4])
        month = int(tstamp[4:6])
        day = int(tstamp[6:8])
        hour = int(tstamp[8:10])
        minute = int(tstamp[10:12])
        second = int(tstamp[12:14])
    except ValueError as err:
        serr = DatetimeError.WithCause(err)

    if not serr.IsError():
        tmonth, serr = ToMonth(month)
        if not serr.IsError():
            datetime = struct_time(tm_year=year, tm_mon=tmonth, tm_day=day, tm_hour=hour, tm_min=minute, tm_sec=second, tm_zone="UTC")

    return datetime, serr
# end def: ToDatetime

def ToMonth(monthNum):
    if monthNum < 1 or monthNum > 12:
        LogWarn("rbacsync", f"Received invalid month number for conversion: {monthNum=}")
        return -1, DatetimeError

    month = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")[monthNum-1]

    return month, NoError
# end def: ToMonth

def ToList(value):
    if value is None:
        return []
    elif isinstance(value, list):
        return value
    else:
        rlist = []
        for item in value.split(","):
            if item.strip() != "":
                rlist.append(item.strip())
        return rlist
# end def: ToList

def LogInfo(tag, message):
    if len(tag) > 0:
        log.appLogger.info("{} - {}".format(tag, message))
    else:
        log.appLogger.info(message)
# end def: LogInfo

def LogError(tag, message, cause):
    if len(tag) > 0:
        log.appLogger.error("{} - {}\n{}".format(tag, message, cause))
    else:
        log.appLogger.error("{}\n{}".format(message, cause))
# end def: LogError

def LogWarn(tag, message, cause=None):
    if len(tag) > 0:
        log.appLogger.warn("{} - {}\n{}".format(tag, message, cause))
    else:
        log.appLogger.warn("{}\n{}".format(message, cause))
# end def: LogWarn
