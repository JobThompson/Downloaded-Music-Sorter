from decouple import config

class ConfigObject:
    def __init__(self):
        pass

    def add_config_value(self, config_value, value):
        value = config(value)
        setattr(self, config_value, value)


class MusicFile:
    def __init__(self, file):
        self.full_name = file
        self.Title = None
        self.Stripped_Title = None
        self.Number = 0
        self.Artists = None
        self.getArtists(file)

    def getArtists(self, file):
        info = file.split(' - ')
        self.Number = info[0]
        self.Artists = info[1]
        self.Title = info[2]
        self.Stripped_Title = info[2].replace('(Explicit)', '')

class Artist:
    def __init__(self, name, song):
        self.name = name
        self.songs = [song]
        