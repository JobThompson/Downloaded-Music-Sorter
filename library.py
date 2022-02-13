class Library:
    def __init__(self, path):
        self.directory_path = path
        self.directories = []
        self.get_directories()
    
    def get_directories(self):
        pass

    def add_directory(self, directory):
        self.directories.append(directory)


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = []

    def get_files(self):
        pass

    def add_file(self, file):
        self.files.append(file)