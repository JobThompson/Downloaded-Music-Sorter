import traceback
from config import config_object
from get_file_metadata import get_file_metadata_mutagen
from file_sorter import FileSorter
from file_comparison import FileComparator
from file_consolidator import FileConsolidator
from library import Library
from music_set import MusicSet
import os
from pprint import pprint
import shutil

FUNCTIONS = {
    1: "Sort files into folders by artist name.",
    2: "Compare two libraries to look for missing artists.",
    3: "Consolidate two libraries into one.",
    4: "Remove duplicates."
}

def get_function():
    while True:
        try:
            print('Select the function you would like to perform:')
            for i in FUNCTIONS:
                print(f'{i}. {FUNCTIONS[i]}')
            selection = input()

            if selection.lower() == 'exit' or selection.lower() == 'quit':
                print('Exiting program...')
                exit()
            elif int(selection) not in FUNCTIONS:
                print('That is not a valid selection, please select from the available options. \n')
            else:
                break
        except ValueError:
            print('That is not a valid selection, please select from the available options. \n')
        except Exception:
            print(traceback.format_exc())
    return int(selection)

def main():
    selection = get_function()
    
    if selection == 1:
        try:
            sorter = FileSorter()
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

    elif selection == 4:
        flac_music_set = MusicSet()
        mp3_music_set = MusicSet()
        duplicates = []
        exceptions_array = []
        onlyfiles = [f for f in  os.listdir(config_object.libraries_to_consolidate)]
        # pprint(onlyfiles)
        # exit()
        for i in onlyfiles:
            file_path = os.path.join(config_object.libraries_to_consolidate, i)
            metadata = get_file_metadata_mutagen(file_path)
            # print(metadata)

           
            
            try:
                title = metadata['title']
                artist = metadata['artist']
            except Exception:
                try:
                    title = metadata['TIT2']
                    artist = metadata['TPE2']
                except Exception:
                    exceptions_array.append(file_path)
                    print(f'{metadata.keys()} {file_path.split(".")[-1]}')
                    continue

            if file_path.split('.')[-1] == 'mp3':
                if mp3_music_set.find_in_set(title, artist):
                    duplicates.append(file_path)
                else:
                    mp3_music_set.add_to_set(title, artist)
            else:
                if flac_music_set.find_in_set(title, artist):
                    duplicates.append(file_path)
                else:
                    flac_music_set.add_to_set(title, artist)
                
        for i in mp3_music_set.title_artist_set:
            if i in flac_music_set.title_artist_set:
                print(f'flac found for {i}')

        for i in duplicates:
            print(f'Deleting {i}')
            os.remove(i)

        # for i in exceptions_array:
        #     file_namespace = '\\'.join(file_path.split('\\')[:-1])
        #     dest = i.replace(file_namespace, 'H:\\Music\\Music\\New folder')
        #     shutil.move(i, dest)
        #     print(f'moved {i}')
            
        
if __name__ == '__main__':
    main()