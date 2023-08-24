import os
from music_file import MusicFile, Artist

class FileSorter:
    def __init__(self) -> None:
        self.artists_array = []
    
    def check_for_artist_folder(self, name, new_repository_path):
        if(not os.path.exists(f'{new_repository_path}/{name}')):
            os.mkdir(f'{new_repository_path}/{name}')
            
    def move_files(self, sort_file_path, new_repository_path):
        for i in self.artists_array:
            for e in i.songs:
                artists_name = (i.name).split(', ')
                self.check_for_artist_folder(artists_name[0], new_repository_path)
                os.replace(f'{sort_file_path}/{e.full_name}',f'{new_repository_path}/{artists_name[0]}/{e.Stripped_Title}')
                
    def sort_files(self, files):
        for i in files:
            artists = []
            for e in self.artists_array:
                artists.append(e.name)
            if i.Artists not in artists:
                self.artists_array.append(Artist(i.Artists, i))
            elif i.Artists in artists:
                self.artists_array[artists.index(i.Artists)].songs.append(i)

    def begin_sort_files(self, sort_file_path, new_repository_path):
        files = [f for f in os.listdir(sort_file_path) if os.path.isfile(os.path.join(sort_file_path, f))]
        for i in files:
            files[files.index(i)] = MusicFile(i)
        self.sort_files(files)
        self.move_files(sort_file_path, new_repository_path)