import traceback
from config import ConfigObject
from file_sorter import FileSorter
from file_comparison import FileComparator
from file_consolidator import FileConsolidator

config = ConfigObject()

FUNCTIONS = {
    1: "Sort files into folders by artist name.",
    2: "Compare two libraries to look for missing artists.",
    3: "Consolidate two libraries into one."
}

CONFIG_VARIABLES = {
    'current_playlist_filepath': "CURRENT_PLAYLIST_FILEPATH",
    'destination_filepath': "DESTINATION_FILEPATH"
}

consolidated_library_path = 'G:\ConsolidatedMusic'
libraries_to_consolidate = 'E:\Music'

ALLOWED_FILETYPES = [ 'mp3', 'mp4', 'flac' ]

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
    sorter = FileSorter()
    
    if selection == 1:
        try:
            if hasattr(config, 'current_playlist_filepath') and hasattr(config, 'destination_filepath'):
                sorter.begin_sort_files(config.current_playlist_filepath, config.destination_filepath)
            else:
                print('Config Value CURRENT_PLAYLIST_FILEPATH or DESTINATION_FILEPATH is missing.')
        except Exception:
            print('Could not sort music.')
            print(traceback.format_exc())

    elif selection == 2:
        comparator = FileComparator()
        comparator.compare_libraries()
        comparator.get_combine_user_answer()
        if comparator.combine_user_answer:
            comparator.combine_libraries()

    elif selection == 3:
        try:
            consolidator = FileConsolidator(libraries_to_consolidate, ALLOWED_FILETYPES)
            consolidator.compare_files()
            consolidator.copy_sorted_files()
                                
        except Exception:
            print('Could not consolidate libraries.')
            print(traceback.format_exc())


if __name__ == '__main__':
    main()