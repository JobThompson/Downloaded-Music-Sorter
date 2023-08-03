import traceback
from music_file import ConfigObject
from library import Library
import sort_files_script
import mutagen
import shutil
from get_file_metadata import get_file_metadata

from pprint import pprint

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
            # PUT LIBRARY CONSOLIDATION HERE
            consolidated_library_path = 'C:\\Users\\pkwp3\\Music\\Consolidated Library'
            library1_path = 'C:\\Users\\pkwp3\\Music\\Music'
            existing_libraries = Library(library1_path)
            files_to_sort = []
            sorted_file_identifiers = []
            sorted_files = []
            
            for i in existing_libraries.get_song_paths_unstripped():
                if i.split('.')[-1:][0] not in ALLOWED_FILETYPES:
                    continue
                try:
                    stats = get_file_metadata(i)
                    print(stats['Filename'])
                    files_to_sort.append(stats)
                except Exception as e:
                    print(f'Could not get metadata for file: {e}')
        
            for i in files_to_sort:
                try:
                    file_name = f'{i["Filename"]}{i["File extension"]}'
                    try:
                        hasInt = int(file_name.split(' - ')[0])
                        file_name = ' - '.join(file_name.split(' - ')[1:])
                    except Exception:
                        pass
                        
                    print(f"{i['Filename']} {i['File extension']} BY: {i['Authors']}")
                    
                    sorted_file_identifier = f"{file_name} BY: {i['Authors']}"
                    if sorted_file_identifier not in sorted_file_identifiers:
                        sorted_file_identifiers.append(sorted_file_identifier)
                        sorted_files.append(f'{i["File location"]}\\{i["Filename"]}{i["File extension"]}')
                        
                except Exception as e:
                    print(f'Could not check if file was duplicate: {e}')
                    
            for i in sorted_files:
                try:
                    file_name = i.split('\\')[-1:][0]
                    try:
                        hasInt = int(file_name.split(' - ')[0])
                        file_name = ' - '.join(file_name.split(' - ')[2:])
                    except Exception:
                        if len(file_name.split(' - ')) > 1:
                            file_name = ' - '.join(file_name.split(' - ')[1:])
                    shutil.copy2(i, f'{consolidated_library_path}\\{file_name}')
                except Exception as e:
                    print(f'Could not copy file: {e}')
                    
        except Exception:
            print('Could not consolidate libraries.')
            print(traceback.format_exc())


        

if __name__ == '__main__':
    main()