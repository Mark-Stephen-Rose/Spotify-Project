class Tal:
    def __init__(self, track_id, account_id):
        self.track_id = track_id
        self.account_id = account_id

    def __repr__(self):
        return f" {str(self.track_id)} {str(self.account_id)}"