import logging

import weather.util.config as cfg

class Logger():
    logger = None
    targetList = ""

    def __init__(self, configFile="./config/logging.ini"):
        global appLogger

        config = cfg.IniConfig(configFile)
        logFile = config.get_value('logFile', 'Logger')
        encType = config.get_value('encoding', 'Logger')
        logLevel = config.get_value('level', 'Logger')
        dateFormat = config.get_value('dateFormat', 'Logger')
        lineFormat = config.get_value('messageFormat', 'Logger')
        self.targetList = config.get_value('target', 'Logger')

        logging.basicConfig(level=logLevel, filename=logFile, encoding=encType, format=lineFormat, datefmt=dateFormat)
        self.logger = logging

        appLogger = self
    # end def: __init__

    def debug(self, message, *argv):
        if self.targetList.find('logFile') > -1:
            self.logger.debug(message, *argv)

        self.printOut(message, *argv)
    # end def: debug

    def info(self, message, *argv):
        if self.targetList.find('logFile') > -1:
            self.logger.info(message, *argv)

        self.printOut(message, *argv)
    # end def: info

    def warn(self, message, *argv):
        if self.targetList.find('logFile') > -1:
            self.logger.warning(message, *argv)

        self.printOut(message, *argv)
    # end def: warn

    def error(self, message, *argv):
        if self.targetList.find('logFile') > -1:
            self.logger.error(message, *argv)

        self.printOut(message, *argv)
    # end def: error

    def printOut(self, message, *argv):
        if self.targetList.find('console') > -1:
            print(message, *argv)
# end class: Logger

appLogger = None
