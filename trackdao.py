import cx_Oracle
from track import Track

class TrackDAO:
  def __init__(self):
    #Establishes a connection to the database
    self.dsn = cx_Oracle.makedsn('csc325.cjjvanphib99.us-west-2.rds.amazonaws.com', 1521, sid="ORCL")
    self.connection = cx_Oracle.connect(user='mrose6', password='csrocks55',dsn=self.dsn)
    # Obtain a cursor
    self.cursor = self.connection.cursor()

  def __del__(self):
    #is a finalizer that will close and disconnect from the database at the end
    self.cursor.close()
    self.connection.close()

  def rowToTrack(self,row):
    track = Track(row[0],row[1],row[2],row[3],row[4],row[5])
    return track

  def trackToRow(self,track):
    row = dict(track_title=track.track_title, track_artist=track.track_artist, track_duration=track.track_duration, track_id=track.track_id, album_id=track.album_id)
    return row

  def insert(self,track):
    sql = "insert into TRACK values (\'" + str(track.track_title) + "\', \'" + str(track.track_artist) + "\', \'" + str(track.track_duration) + "\', \'" + str(track.track_id) + "\', \'" + str(track.album_id) + "\')"
    self.cursor.execute(sql)
    self.connection.commit()

  def delete(self, track):
    sql = "delete from TRACK where track_id='" + str(track.track_id) + "'"
    self.cursor.execute(sql)
    self.connection.commit()

  def deleteAll(self):
    sql = "delete from TRACK"
    self.cursor.execute(sql)
    self.connection.commit()

  def selectAll(self):
    sql = "select * from TRACK"
    self.cursor.execute(sql)
    tracks=[]
    while True:
      row = self.cursor.fetchone()
      if row is None:
        break
      track = self.rowToTrack(row)
      tracks.append(track)
    return tracks

  def selectById(self,id):
    sql = "select * from TRACK where track_id='" + str(id) + "'"
    self.cursor.execute(sql)
    row = self.cursor.fetchone()
    if row!= None:
      track = self.rowToTrack(row)
      return track
    return None

  def update(self, track):
    sql = str("update TRACK set track_title=\'" + str(track.track_title) + "\', track_artist=\'" + str(track.track_artist) + "\', track_id=\'" + str(track.track_id) + "\', album_id=\'" + str(track.album_id) + "\' where track_id='" + str(track.track_id) + "'")
    self.cursor.execute(sql)
    self.connection.commit()

  def testSQL(self, track):
    insert = "insert into TRACK values (\'" + str(track.track_title) + "\', \'" + str(track.track_artist) + "\', \'" + str(track.track_duration) + "\', \'" + str(track.track_id) + "\', \'" + str(track.album_id) + "\')"
    print(insert)
    delete = "delete from TRACK where track_id='" + str(track.track_id) + "'"
    print(delete)
    update = str("update TRACK set track_title=\'" + str(track.track_title) + "\', track_artist=\'" + str(track.track_artist) + "\', track_id=\'" + str(track.track_id) + "\', album_id=\'" + str(track.album_id) + "\' where track_id='" + str(track.track_id) + "'")
    print(update)

