"""
Package app_config consolidates and provides access to application configuration
data through the following methods with the given order of precedence (highest
to lowest):

 1. command line arguments, e.g.: --testMode=true
 2. environment variables, e.g.: APP_TEST_MODE=true
 3. configuration file properties, e.g.: app.testMode=true

The configuration parser is itself configured through parser configuration file
at: ./config/parameters.ini, relative to the project root. The parser
configuration file has the following structure:

[Meta]
applicationName = rbacsync
applicationDescriptionFile = ./config/description.txt
applicationVersion = alpha-SNAPSHOT
applicationDate = current
argSwitch = --
argSeparator = EQUALS
parameterNames = help,...

[Parameters]
help_cliArgument = help
help_environmentVar = SHOW_USAGE
help_propertyName = showUsage
help_defaultVal = userMustProvide
help_description = Show this usage information.
...

Once parser is successfully configured, the package looks for its default
application configuration file at: ./config/<applicationName>.ini, relative to
the project root. Once parsing is complete, the package presents a unified view
of the application configuration through its AssignedValue, ValueOf, and
ValueOfWithDefault methods.

Assign a value of 'userMustProvide' to a parameter to define an option with no
value as opposed to an option with an empty value.

The following shows a sample usage:

    import ./classes/app_config as cfg
    ...
    loaded, err = cfg.Parse()
    if !loaded:
        log.Fatal(fmt.Sprintf("Error parsing runtime parameters: %v", err))

    optionId := "testModeKey"
    if cfg.AssignedValue(optionId) {
        testMode := cfg.ValueOf(optionId)
    } else {
        testMode := cfg.ValueOfWithDefault(optionId, "false")
    }
"""

import os, sys

import weather.util.config as cfg

from collections import namedtuple
from collections.abc import Mapping

from weather.util.utils import LoadTextFile, ParseOptions

# Constant HELP_ID provides the default usage request argument identifier.
HELP_ID = "help"

# Constant APP_CONFIG_ID provides the default config file argument
# identifier.
APP_CONFIG_ID = "configFile"

# Constant PARSER_CONFIG_FILE provides the default location of the parser
# configuration file, relative to the 'config' package.
PARSER_CONFIG_FILE = "./config/parameters.ini"

# Constant APPLICATION_CONFIG_FILE provides the default location of the
# application configuration file, relative to the 'config' package.
APPLICATION_CONFIG_FILE = "./config/app_config.ini"

# Constant USER_MUST_PROVIDE ("userMustProvide") serves as default value
# for any parameter not assigned a value through configuration and which is
# not otherwise assigned a default value.
USER_MUST_PROVIDE = "userMustProvide"

# Usage output formats
FLAG_LINE_FORMAT   = "{}{}"
SWITCH_LINE_FORMAT = "{}{}{}<value>"
DESCRIPTION_FORMAT = "  {}\n"
ALTERNATIVE_FORMAT = "  [variable: {}; property: {}]"

# Parameter represents application options.
Parameter = namedtuple('Parameter', [
    'optionId', 'cliArgument', 'environmentVar',
    'propertyName', 'defaultVal', 'description'])
# end class: Parameter

# ParserConfig represents a loaded and parsed configuration chain. Field
# 'ArgSeparator' must be one of: "SPACE", "EQUALS", "COMMA", "COLON",
# "SEMI-COLON" (default is SPACE)
ParserConfig = {
    'applicationName': "",
    'applicationDescriptionFile': "",
    'applicationVersion': "",
    'applicationDate': "",

    # CLI argument prefix switch (e.g. "--")
    'argSwitch': "",

    # CLI argument separator character (one of: SPACE [' '], COMMA [','], COLON [':'], SEMI-COLON [';'])
    'argSeparator': "",

    'parameterNames': [],
    'parameters': Mapping[str, Parameter]
}
ParserConfig['parameters'] = {}

# A configuration containing a loaded and parsed application configuration
# chain (see ApplicationConfig.Parse).
Config = {
    # internal parser configuration instance
    'parserConfig': ParserConfig,

    # flag configuration is loaded
    'parserLoaded': False
}

# A lookup dict for argSeparator config values
ArgSeparators = {
    'SPACE': ' ',
    'EQUALS': '=',
    'COMMA': ',',
    'COLON': ':',
    'SEMI-COLON': ';'
}

def LoadParserConfig(filePath):
    global Config, ParserConfig

    iniFile = cfg.IniConfig(filePath)

    # Load 'Meta' section...
    for key in ('applicationName', 'applicationDescriptionFile',
             'applicationVersion', 'applicationDate',
             'argSwitch', 'argSeparator'):
        ParserConfig[key] = iniFile.get_value(key, 'Meta')

    ParserConfig['parameterNames'] = iniFile.get_value('parameterNames', 'Meta').split(",")

    # Load 'Parameters' section...
    for parm in ParserConfig['parameterNames']:
        cliArgument = iniFile.get_value("{}_cliArgument".format(parm), 'Parameters')
        environmentVar = iniFile.get_value("{}_environmentVar".format(parm), 'Parameters')
        propertyName = iniFile.get_value("{}_propertyName".format(parm), 'Parameters')
        defaultVal = iniFile.get_value("{}_defaultVal".format(parm), 'Parameters')
        description = iniFile.get_value("{}_description".format(parm), 'Parameters')

        ParserConfig['parameters'][parm] = Parameter(
            parm, cliArgument, environmentVar, propertyName, defaultVal, description)

    Config['parserLoaded'] = True
# end def: LoadParserConfig

class ApplicationConfig:
    """
    ApplicationConfig represents a loaded and parsed application configuration.
    """
    parserConfigPath = ""
    applicationConfigPath = ""
    applicationConfig = {}

    def __init__(self):
        """
        Initializes the application configuration...
        """
        if 'ParserConfigPath' in os.environ:
            self.parserConfigPath = os.environ['ParserConfigPath']
        else:
            self.parserConfigPath = PARSER_CONFIG_FILE

        if 'ApplicationConfigPath' in os.environ:
            self.applicationConfigPath = os.environ['ApplicationConfigPath']
        else:
            self.applicationConfigPath = APPLICATION_CONFIG_FILE

        self._parse()
    # end def: __init__

    def SetValueOf(self, key, value):
        self.applicationConfig[key] = value
    # end def: SetValue

    def ValueOf(self, key):
        """
        Returns the value of the specified configuration key. Returns null
        ('None') if the key isn't found.
        """
        global Config

        if key in self.applicationConfig:
            return self.applicationConfig[key]

        return ""
    # end def: ValueOf

    def ValueOfWithDefault(self, key, value):
        """
        Returns the value of the specified configuration key. Returns the given
        value if the key isn't found.
        """
        parmVal = self.ValueOf(key)
        if parmVal == USER_MUST_PROVIDE:
            parmVal = value

        return parmVal
    # end def: ValueOfWithDefault

    def AssignedValue(self, key):
        """
        Returns True if the specified configuration key has a user assigned
        (i.e. not empty and not assigned value "userMustProvide". Otherwise,
        returns False.
        """
        if key in self.applicationConfig and self.applicationConfig[key] != USER_MUST_PROVIDE:
            return True
        
        return False
    # end def: AssignedValue

    def IsParsed(self):
        """
        Returns True if the application configuration is loaded and parsed.
        Otherwise, returns False.
        """
        global Config

        return Config['parserLoaded']
    # end def: IsParsed

    def Usage(self):
        """
        Displays configuration usage information on the console.
        """
        global ArgSeparators, ParserConfig

        print(f"{ParserConfig['applicationName']}, version {ParserConfig['applicationVersion']} {ParserConfig['applicationDate']}\n")
        print(f"{LoadTextFile(ParserConfig['applicationDescriptionFile'])}")
        print("\nUsage:")
        parms: Mapping[str, Parameter] = ParserConfig['parameters']

        for option in parms:
            if parms[option].cliArgument == "help":
                print(FLAG_LINE_FORMAT.format(ParserConfig['argSwitch'], parms[option].cliArgument))
            else:
                print(SWITCH_LINE_FORMAT.format(ParserConfig['argSwitch'], parms[option].cliArgument, ArgSeparators.get(ParserConfig['argSeparator'])))
            print(ALTERNATIVE_FORMAT.format(parms[option].environmentVar, parms[option].propertyName))
            print(DESCRIPTION_FORMAT.format(parms[option].description))
    # end def: Usage

    def _parse(self):
        """
        Loads and parses the application configuration and returns True if loaded with no errors.
        Otherwise, returns False.
        """
        global ArgSeparators, Config, ParserConfig

        if not Config['parserLoaded']:
            # Load the parser configuration
            LoadParserConfig(self.parserConfigPath)

            # Set the values with preference for CLI options, followed by env
            # overrides...
            options = ParseOptions(ParserConfig['argSwitch'], ArgSeparators.get(ParserConfig['argSeparator']), sys.argv[1:])
            updateProps = []
            parmVal = ""
            for opt in ParserConfig['parameters']:
                parm = ParserConfig['parameters'][opt]
                if parm.cliArgument in options:
                    parmVal = options[parm.cliArgument]
                elif os.getenv(parm.environmentVar) != None:
                    parmVal = os.getenv(parm.environmentVar)
                else:
                    parmVal = parm.defaultVal
                    updateProps.append(parm.optionId)
                self.applicationConfig[parm.optionId] = parmVal

            if self.AssignedValue(APP_CONFIG_ID) or len(self.applicationConfigPath) > 0:
                # ...after which, configuration properties can define any parameters
                # not already assigned.
                appFilePath = self.applicationConfigPath
                if self.AssignedValue(APP_CONFIG_ID):
                    appFilePath = self.ValueOf(APP_CONFIG_ID)
                appFile = cfg.IniConfig(appFilePath)
                for option in updateProps:
                    val = appFile.get_value(ParserConfig['parameters'][option].propertyName, "Main")
                    if val != None:
                        self.applicationConfig[option] = val

        if self.AssignedValue(HELP_ID):
            self.Usage()
            sys.exit()

        return True
    # end def: _parse
# end class: ApplicationConfig
