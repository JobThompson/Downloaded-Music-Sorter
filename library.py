import os
from pprint import pprint

class Directory:
    def __init__(self, name, path):
        self.name = name
        self.path = path + "\\" + self.name
        self.songs = []
        self.check_for_directories()

        if hasattr(self, 'directories') != True:
            self.files = []
            self.get_files()
            self.get_file_unstripped()
        else:
            self.get_directories()

    def check_for_files(self):
        if hasattr(self, 'files') != True:
            return False
        else:
            return True

    def return_songs(self):
        self.songs = []
        if hasattr(self, 'files') != True:
            for i in self.directories:
                songs = i.return_songs()
                for e in songs:
                    self.songs.append(e)
            return self.songs
        else:
            return self.files

    def return_song_paths(self):
        self.song_paths = []
        if hasattr(self, 'files') != True:
            for i in self.directories:
                songs = i.return_song_paths()
                for e in songs:
                    self.song_paths.append(self.name + '\\' + e)
            return self.song_paths
        else:
            for i in self.files:
                self.song_paths.append(self.name + '\\' + i)
            return self.song_paths
        
    def return_song_paths_unstripped(self):
        self.song_paths_unstripped = []
        if hasattr(self, 'unstripped_files') != True:
            for i in self.directories:
                songs = i.return_song_paths_unstripped()
                for e in songs:
                    self.song_paths_unstripped.append(self.name + '\\' + e)
            return self.song_paths_unstripped
        else:
            for i in self.unstripped_files:
                self.song_paths_unstripped.append(self.name + '\\' + i)
            return self.song_paths_unstripped
        
    def check_for_directories(self):
        directories = [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
        if directories != []:
            self.hasFolders = True
            self.directories = directories
        else:
            self.hasFolders = False
            
    def get_directories(self):
        for i in self.directories:
            self.directories[self.directories.index(i)] = Directory(i, self.path)

    def get_files(self):
        self.files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for i in self.files:
            array = i.split(' - ')
            if len(array) <= 2:
                pass
            else:
                self.files[self.files.index(i)] = array[2].replace('(Explicit)', '')
                
    def get_file_unstripped(self):
         self.unstripped_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    def add_file(self, file):
        self.files.append(file)

class Library:
    def __init__(self, path):
        self.path = path
        self.list_of_directories = [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
        for i in self.list_of_directories:
            self.list_of_directories[self.list_of_directories.index(i)] = Directory(i, self.path)
        self.list_of_directories.append(Directory('', self.path))
        self.songs = []
        self.get_songs()

    def get_songs(self):
        for i in self.list_of_directories:
            songs = i.return_songs()
            for e in songs:
                self.songs.append(e)
    
    def get_song_paths(self):
        song_paths = []
        for i in self.list_of_directories:
            song_path = i.return_song_paths()
            for e in song_path:
                song_paths.append(self.path + '\\' + e)
        return song_paths
    
    def get_song_paths_unstripped(self):
        song_paths = []
        for i in self.list_of_directories:
            song_path = i.return_song_paths_unstripped()
            for e in song_path:
                song_paths.append(self.path + '\\' + e)
        return song_paths


