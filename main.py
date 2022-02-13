import os
import traceback
from music_file import ConfigObject
import sort_files_script

config = ConfigObject()

# pip install python-magic 
# pip install python-decouple

FUNCTIONS = {
    1: "Sort files into folders by artist name.",
    2: "Compare two libraries to look for missing artists.",
    3: "Compare two libraries to look for missing songs."
}

CONFIG_VARIABLES = {
    'current_playlist_filepath': "CURRENT_PLAYLIST_FILEPATH",
    'destination_filepath': "DESTINATION_FILEPATH"
}

def get_config():
    for i in CONFIG_VARIABLES:
        try:
            config.add_config_value(i, CONFIG_VARIABLES[i] )
        except Exception:
            print(f'Could not get config value for {CONFIG_VARIABLES[i]}.')

def get_function():
    while True:
        print('Select the function you would like to perform:')
        for i in FUNCTIONS:
            print(f'{i}. {FUNCTIONS[i]}')
        selection = input()

        if selection.lower() == 'exit' or selection.lower() == 'quit':
            exit()
        elif int(selection) not in FUNCTIONS:
            print('That is not a valid selection, please select from the avaliable options. \n')
        else:
            break

    return int(selection)

def main():
    get_config()
    selection = get_function()
    if selection == 1:
        try:
            if hasattr(config, 'current_playlist_filepath') and hasattr(config, 'destination_filepath'):
                sort_files_script.sort_files_script(config.current_playlist_filepath, config.destination_filepath)
            else:
                print('Config Value CURRENT_PLAYLIST_FILEPATH or DESTINATION_FILEPATH is missing.')
        except Exception:
            print('Could not sort music.')
            print(traceback.format_exc())

    elif selection == 2:
        try:
            # PUT LIBRARY ARTIST COMPARISON HERE
            pass
        except Exception:
            print('Could not compare libraries.')
            print(traceback.format_exc())

    elif selection == 3:
        try:
            # PUT LIBRARY SONG COMPARISON HERE
            pass
        except Exception:
            print('Could not compare libraries.')
            print(traceback.format_exc())

        

if __name__ == '__main__':
    main()