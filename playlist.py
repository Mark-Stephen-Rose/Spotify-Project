class Playlist:
    def __init__(self, playlist_title, total_playlist_tracks, playlist_id, account_id):
        self.playlist_title = playlist_title
        self.total_playlist_tracks = total_playlist_tracks
        self.playlist_id = playlist_id
        self.account_id = account_id

    def __repr__(self):
        return f" {str(self.playlist_title)} {str(self.total_playlist_tracks)} {str(self.playlist_id)} {str(self.account_id)}"