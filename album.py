class Album:
  def __init__(self, album_id, account_id):
    self.album_id = album_id
    self.account_id = account_id

  def __repr__(self):
    return f" {str(self.album_id)} {str(self.account_id)}"