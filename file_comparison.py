from library import Library
from pprint import pprint
import os
import mutagen
import shutil

class FileComparator:
    def __init__(self, library1_path, library2_path) -> None:
        self.combine_user_answer = False
        self.library1_path = library1_path | input('Enter filepath for the first library: ')
        self.library2_path = library2_path | input('Enter filepath for the second library: ')
        self.missing_songs = []
        self.combined_list = []
        self.library_one = Library(self.library1_path)
        self.library_two = Library(self.library2_path)
        
    def check_for_artist_folder(self, name, new_repository_path):
        if(not os.path.exists(f'{new_repository_path}/{name}')):
            os.mkdir(f'{new_repository_path}/{name}')
        
    def compare_libraries(self):
        for i in self.library_one.songs:
                if i not in self.library_two.songs and i not in self.missing_songs:
                    self.missing_songs.append(i)
                if i not in self.combined_list:
                    self.combined_list.append(i)
            
        for i in self.library_two.songs:
            if i not in self.library_one.songs and i not in self.missing_songs:
                self.missing_songs.append(i)
            if i not in self.combined_list:
                self.combined_list.append(i)

        pprint(self.missing_songs)
        
    def get_combine_user_answer(self):
        print('Do you want to combine these libraries? Y/N')
        response = input().lower()
        if response == 'y':
            self.combine_user_answer = True
        elif response == 'n':
            self.combine_user_answer = False
        else:
            print('That is not a valid selection.')
            self.get_combine_user_answer()
            

    def combine_libraries(self):
        print('Where do you want the combined library to be stored? Enter the full filepath.')
        destination_filepath = input()
        lib1_paths = self.library_one.get_song_paths()
        [lib1_paths.append(i) for i in self.library_two.get_song_paths()]            
                
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
                    artist = 'Unknown'
                artist = artist.replace('/', '-').replace('*', '-').replace(':', '-').replace('"', '').replace('?', '')

                if array[len(array)-1] not in self.combined_list:
                    pass
                else:
                    try:
                        self.check_for_artist_folder(artist, destination_filepath)
                        title = title.replace('"', '').replace('?', '').replace('/', '-').replace(':', '-').replace('*', '-')
                        shutil.copy2(i, f'{destination_filepath}/{artist}/{title}{filetype}')
                        self.combined_list.pop(self.combined_list.index(array[len(array)-1]))
                    except Exception:
                        pass
                    else:
                        pass