from decouple import config

CONFIG_VARIABLES = {
    'current_playlist_filepath': "CURRENT_PLAYLIST_FILEPATH",
    'destination_filepath': "DESTINATION_FILEPATH",
    'consolidated_library_path': "CONSOLIDATED_LIBRARY_PATH",
    'libraries_to_consolidate': "LIBRARIES_TO_CONSOLIDATE",
    'allowed_filetypes': "ALLOWED_FILE_TYPES",
}

class ConfigObject:
    def __init__(self):
        self.get_config()

    def add_config_value(self, config_value, value):
        value = config(value)
        setattr(self, config_value, value) 

    def get_config(self):
        for i in CONFIG_VARIABLES:
            try:
                self.add_config_value(i, CONFIG_VARIABLES[i] )
            except Exception:
                print(f'Could not get config value for {CONFIG_VARIABLES[i]}.')
                
                
config_object = ConfigObject()