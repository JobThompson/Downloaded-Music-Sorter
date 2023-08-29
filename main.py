import traceback
from config import config_object
from file_sorter import FileSorter
from file_comparison import FileComparator
from file_consolidator import FileConsolidator

FUNCTIONS = {
    1: "Sort files into folders by artist name.",
    2: "Compare two libraries to look for missing artists.",
    3: "Consolidate two libraries into one."
}

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
    selection = get_function()
    sorter = FileSorter()
    
    if selection == 1:
        try:
            if hasattr(config_object, 'current_playlist_filepath') and hasattr(config_object, 'destination_filepath'):
                sorter.begin_sort_files(config_object.current_playlist_filepath, config_object.destination_filepath)
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
            consolidator = FileConsolidator(config_object.libraries_to_consolidate, config_object.allowed_filetypes.split(','))
            consolidator.compare_files()
            consolidator.copy_sorted_files()
                                
        except Exception:
            print('Could not consolidate libraries.')
            print(traceback.format_exc())


if __name__ == '__main__':
    main()