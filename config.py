from decouple import config

class ConfigObject:
    def __init__(self):
        pass

    def add_config_value(self, config_value, value):
        value = config(value)
        setattr(self, config_value, value)