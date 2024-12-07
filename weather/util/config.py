"""
Config provides read/write access to configuration files in .ini, .json, and
.properties formats.

One class for each configuration file type is provided with functions to get a
value, set/update a value, and save values to disk, i.e.:
* IniConfig
* JsonConfig
* PropertiesConfig

Each takes a filename argument to load and/or save, e.g.:

import config as cfg
# Open a config file (.ini); if file does not exist, create it...
config = cfg.IniConfig('my-config-file.ini')

# Read a value, return None if key does not exist...
# 'section' is optional and defaults to None
value = config.get_value('key', 'section')

# Set/update a value, returning prior value or None if setting a new key...
# 'section' is optional and defaults to None
old_value = config.set_value('key', 'NewValue', 'section')

# Save values to file, returing True on success or False on error...
success = config.save()
"""
#import json
import configparser as ini


class Config:
    """Base config class. Should not be used directly."""

    def __init__(self, filename) -> None:
        """
        Initializes the instance by opening the file and loading it's values.
        """
        self.filename = filename
        self.config_map = self.load()
    # End: def Config.__init__

    def get_value(self, key, section=''):
        """
        Returns the value bound to key in the config. If section is provided
        then the key is looked for in the given section. Returns None if key
        or section doesn't exist.
        """
        value = None

        if section and section in self.config_map:
            config = self.config_map[section]
        else:
            config = self.config_map
        
        if key in config:
            value = config[key]

        return value
    # End: def Config.get_value

    def set_value(self, key, value, section=''):
        """
        Binds the given value to the specified key. If a value is already bound
        to the key then the previous value is returned. Otherwise None is
        returned. If section is provided then the key is updated in the
        specified section. If the section doesn't exist then it is created.
        """
        old_value = self.get_value(key, section)

        if section:
            if section in self.config_map:
                config = self.config_map[section]
            else:
                config = {}
                self.config_map[section] = config
        else:
            config = self.config_map

        config[key] = value

        return old_value
    # End: def Config.set_value

    def save(self):
        """
        Saves the configuration to the named file on disk.
        """
        pass
    # End: def Config.save

    def load(self):
        """
        Loads the named configuration file from disk.
        """
        pass
    # End: def Config.load
# End: class Config


class IniConfig(Config):
    """Config class for reading and writing files in .ini format."""

    def __init__(self, filename) -> None:
        global config

        super().__init__(filename)
        config = self
    # End: def IniConfig.__init__

    def save(self):
        parser = ini.ConfigParser()
        for key in self.config_map:
            parser[key] = self.config_map[key]

        with open(self.filename, 'w') as f:
            parser.write(f)
    # End: def IniConfig.save

    def load(self):
        config = {}

        try:
            parser = ini.ConfigParser()
            files = parser.read(self.filename)
        except ini.MissingSectionHeaderError as e:
            msg = e.message
            print(f"Ini file {self.filename} is improperly formatted:\n{msg}.")
        else:
            if self.filename in files:
                for section in parser.sections():
                    config[section] = parser[section]

        return config
    # End: def IniConfig.load
# End: class IniConfig


def get_config_value(config, key, section):
    return config.get_value(key, section)
# End: def get_config_value

def get_config_value_default(config, key, section, default=None):
    value = get_config_value(config, key, section)
    if value is None:
        value = default
    return value
# End: def get_config_value_default
