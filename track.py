class Track:
  def __init__(self, track_title, track_artist, track_duration, track_id, album_id):
    self.track_title = track_title
    self.track_artist = track_artist
    self.track_duration = track_duration
    self.track_id = track_id
    self.album_id = album_id

  def __repr__(self):
    return f" {str(self.track_title)} {str(self.track_artist)} {str(self.track_duration)} {str(self.track_id)} {str(self.album_id)}"