class MusicSet():
    def __init__(self) -> None:
        self.title_artist_set = set([])
        
    def add_to_set(self, title, artist):
        self.title_artist_set.add(f'{title}: {artist}'.lower())
        
    def find_in_set(self, title, artist):
        if len(self.title_artist_set) > 0:
            return f'{title}: {artist}'.lower() in self.title_artist_set
        else:
            return False