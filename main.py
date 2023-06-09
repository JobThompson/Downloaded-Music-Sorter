from math import comb
import os
import traceback
from music_file import ConfigObject
from library import Library
import sort_files_script
import mutagen
import shutil

from pprint import pprint

config = ConfigObject()

# pip install python-magic 
# pip install python-decouple
# pip install mutagen

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
        # library1_path = 'D:\Music\Tidal\Artists'
        # library2_path = 'I:\Music\Music Files'
        library1_path = input('Enter filepath for the first library: ')
        library2_path = input('Enter filepath for the second library: ')

        try:
            missing_songs = []
            combined_list = []
            library_one = Library(library1_path)
            library_two = Library(library2_path)

            for i in library_one.songs:
                if i not in library_two.songs and i not in missing_songs:
                    missing_songs.append(i)
                if i not in combined_list:
                    combined_list.append(i)
            
            for i in library_two.songs:
                if i not in library_one.songs and i not in missing_songs:
                    missing_songs.append(i)
                if i not in combined_list:
                    combined_list.append(i)

            pprint(missing_songs)

            print('Do you want to combine these libraries? Y/N')
            response = input().lower()

            if response == 'y':
                print('Where do you want the combined library to be stored? Enter the full filepath.')
                destination_filepath = input()
                lib1_paths = library_one.get_song_paths()
                lib2_paths = library_two.get_song_paths()

                for i in lib2_paths:
                    lib1_paths.append(i)
                
                for i in lib1_paths:
                    array = i.split('\\')
                    music_details = mutagen.File(i)
                    music_details.save()

                    if '.mp3' in i.lower():
                        filetype = '.mp3'
                    elif '.mp4' in i.lower():
                         filetype = '.mp4'
                    elif '.flac' in i.lower():
                         filetype = '.flac'
                    else: 
                        filetype = '.flac'

                    if music_details is not None:
                        try:
                            artist = music_details['artist'][0]
                        except Exception:
                            artist = 'Unknown'
        
                        try:
                            title = music_details['title'][0]
                        except Exception:
                            title = 'Unknown'
                        
                        if artist == '':
                            artist = 'Unkown'
                        artist = artist.replace('/', '-').replace('*', '-').replace(':', '-').replace('"', '').replace('?', '')

                        if array[len(array)-1] not in combined_list:
                            pass
                        else:
                            try:
                                sort_files_script.check_for_artist_folder(artist, destination_filepath)
                                title = title.replace('"', '').replace('?', '').replace('/', '-').replace(':', '-').replace('*', '-')
                                shutil.copy2(i, f'{destination_filepath}/{artist}/{title}{filetype}')
                                combined_list.pop(combined_list.index(array[len(array)-1]))
                            except Exception:
                                pass
                    else:
                        pass

            elif response == 'n':
                pass
            else:
                print('That is not a valid selection.')
            print('Program will now terminate.')
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