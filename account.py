class Account:
  def __init__(self,email, username, id):
    self.email = email
    self.username = username
    self.id = id

  def __repr__(self):
    return f" {self.email} {self.username} {str(self.id)}"
