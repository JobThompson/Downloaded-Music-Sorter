import os
from music_file import MusicFile, Artist

Artists_Array = []

def check_for_artist_folder(name, new_repository_path):
    if(not os.path.exists(f'{new_repository_path}/{name}')):
        os.mkdir(f'{new_repository_path}/{name}')

def move_files(sort_file_path, new_repository_path):
    for i in Artists_Array:
        for e in i.songs:
            artists_name = (i.name).split(', ')
            check_for_artist_folder(artists_name[0], new_repository_path)
            os.replace(f'{sort_file_path}/{e.full_name}',f'{new_repository_path}/{artists_name[0]}/{e.Stripped_Title}')
            
def sort_files(files):
    for i in files:
        artists = []
        for e in Artists_Array:
            artists.append(e.name)
        if i.Artists not in artists:
            Artists_Array.append(Artist(i.Artists, i))
        elif i.Artists in artists:
            Artists_Array[artists.index(i.Artists)].songs.append(i)

def sort_files_script(sort_file_path, new_repository_path):
    files = [f for f in os.listdir(sort_file_path) if os.path.isfile(os.path.join(sort_file_path, f))]
    for i in files:
        files[files.index(i)] = MusicFile(i)
    sort_files(files)
    move_files(sort_file_path, new_repository_path)