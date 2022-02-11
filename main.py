import os
from decouple import config
from music_file import MusicFile, Artist

Artists_Array = []

def check_for_artist_folder(name, new_file_path):
    if(not os.path.exists(f'{new_file_path}/{name}')):
        os.mkdir(f'{new_file_path}/{name}')

def move_files(file_path, new_file_path):
    for i in Artists_Array:
        for e in i.songs:
            artists_name = (i.name).split(', ')
            check_for_artist_folder(artists_name[0], new_file_path)
            os.replace(f'{file_path}/{e.full_name}',f'{new_file_path}/{artists_name[0]}/{e.Stripped_Title}')
            

def sort_files(music):
    for i in music:
        artists = []
        for e in Artists_Array:
            artists.append(e.name)
        if i.Artists not in artists:
            Artists_Array.append(Artist(i.Artists, i))
        elif i.Artists in artists:
            Artists_Array[artists.index(i.Artists)].songs.append(i)

def get_filepath():
    file_path = config('FILEPATH')
    new_file_path = config('NEWFILEPATH')
    return file_path, new_file_path

def main():
    file_path, new_file_path = get_filepath()
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    music = []
    for i in files:
        music.append(MusicFile(i))
    sort_files(music)
    move_files(file_path, new_file_path)
        

if __name__ == '__main__':
    main()