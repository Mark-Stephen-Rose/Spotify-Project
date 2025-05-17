import cx_Oracle
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from album import Album

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class AlbumDAO:
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

  def rowToAlbum(self,row):
    album = Album(row[0],row[1])
    return album

  def albumToRow(self,album):
    row = dict(album_id=album.album_id, account_id=album.account_id)
    return row

  def insert(self, album):
    album_row = self.albumToRow(album)
    sql = "INSERT INTO ALBUM VALUES (:album_id, :account_id)"
    self.cursor.execute(sql, album_row)
    self.connection.commit()

  def delete(self, album):
    sql = "delete from ALBUM where album_id='" + str(album.album_id) + "'"
    self.cursor.execute(sql)
    self.connection.commit()

  def deleteAll(self):
    sql = "delete from ALBUM"
    self.cursor.execute(sql)
    self.connection.commit()

  def selectAll(self):
    sql = "select * from ALBUM"
    self.cursor.execute(sql)
    albums=[]
    while True:
      row = self.cursor.fetchone()
      if row is None:
        break
      album = self.rowToAlbum(row)
      albums.append(album)
    return albums

  def selectByAlbumId(self,id):
      sql = "select * from ALBUM where album_id='" + str(id) + "'"
      self.cursor.execute(sql)
      row = self.cursor.fetchone()
      if row is not None:
          album = self.rowToAlbum(row)
          return album
      return None

  def selectByUserId(self, userid):
    sql = "select * from ALBUM where account_id='" + str(userid) + "'"
    self.cursor.execute(sql)
    rows = self.cursor.fetchall()

    albums = []
    for row in rows:
        album = self.rowToAlbum(row)
        if album is not None:
            albums.append(album)
    return albums

  def selectAlbumAndAccount(self,id,userid):
    sql = "select * from ALBUM where album_id='" + str(id) + "' AND account_id='" + userid + "'"
    self.cursor.execute,(sql)
    row = self.cursor.fonehone()
    if row is not None:
        album = self.rowToAlbum(row)
        return album
    return None

  def update(self, album):
    sql = str("update ALBUM set album_id=\'" + str(album.album_id) + "\' where album_id='" + str(album.album_id) + "'")
    self.cursor.execute(sql)
    self.connection.commit()

  def testSQL(self, album):
    sql = "insert into ALBUM values (\'" + str(album.album_title) + "\', \'" + str(album.album_artist) + "\', \'" + str(album.release_date) + "\', \'" + album.total_tracks + "\', \'" + str(album.album_id) +"\')"
    print(sql)
    delete = "delete from ALBUM where album_id='" + str(album.album_id) + "'"
    print(delete)
    update = str("update ALBUM set album_title=\'" + str(album.album_title) + "\', album_artist=\'" + str(album.album_artist) + "\', release_date=\'" + str(album.release_date) + "\', total_tracks=\'" + album.total_tracks + "\', album_id=\'" + str(album.album_id) + "\' where album_id='" + str(album.album_id) + "'")
    print(update)

  def getAlbums(self, sp, userid):
    saved_albums = sp.current_user_saved_albums()

    for item in saved_albums['items']:
      album_data = item['album']
      album_id = album_data['id']
      account_id = userid

      album = Album(album_id, account_id)
      
      existing_album = self.selectByAlbumId(album_id)
      if existing_album is None:
          self.insert(album)

  def getAlbumById(self,sp,albumid):
    
    logging.debug("before sp gets called")
    album = sp.album(albumid)
    logging.debug("Album in getAlbumById " + str(album))
    return album

  def getAlbumsFromAlbumId(self, album, album_id, userid):
    album_title = album['name']
    album_artist = ", ".join([artist['name'] for artist in album['artists']])
    release_date = album['release_date']
    total_tracks = album['total_tracks']
    account_id = userid
    
    album_info ={'album_title': album_title,
      'album_artist': album_artist,
      'release_date': release_date,
      'total_tracks': total_tracks,
      'account_id': userid,  
      'album_id': album_id}
    
    return album_info
