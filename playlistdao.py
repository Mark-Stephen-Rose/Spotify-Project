import cx_Oracle
from playlist import Playlist
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class PlaylistDAO:
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

    def rowToPlaylist(self,row):
        playlist = Playlist(row[0],row[1],row[2],row[3])
        return playlist

    def playlistToRow(self,playlist):
        row = dict(playlist_title=playlist.playlist_title, total_playlist_tracks=playlist.total_playlist_tracks, playlist_id=playlist.playlist_id, account_id=playlist.account_id)
        return row

    def insert(self,playlist):
        sql = "insert into PLAYLIST values (\'" + str(playlist.playlist_title) + "\', \'" + str(playlist.total_playlist_tracks) +  "\', \'" + str(playlist.playlist_id) + "\', \'" + str(playlist.account_id) + "\')"
        self.cursor.execute(sql)
        self.connection.commit()

    def delete(self, id):
        sql = "delete from PLAYLIST where playlist_id='" + str(id) + "'"
        self.cursor.execute(sql)
        self.connection.commit()

    def deleteAll(self):
        sql = "delete from PLAYLIST"
        self.cursor.execute(sql)
        self.connection.commit()

    def selectAll(self):
        sql = "select * from PLAYLIST"
        self.cursor.execute(sql)
        playlists=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            playlist = self.rowToPlaylist(row)
            playlists.append(playlist)
        return playlists

    def selectByPlaylistId(self,id):
        sql = "select * from PLAYLIST where playlist_id='" + str(id) + "'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row!= None:
            user = self.rowToPlaylist(row)
            return user
        return None

    def selectByUserId(self, userid):
        sql = "select * from PLAYLIST where account_id='" + str(userid) + "'"
        self.cursor.execute(sql)
        playlists=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            playlist = self.rowToPlaylist(row)
            playlists.append(playlist)
        return playlists

    def update(self, playlist):
        sql = str("update PLAYLIST set total_playlist_tracks=\'" + str(playlist.total_playlist_tracks) + "\' where playlist_id='" + str(playlist.playlist_id) + "'")
        self.cursor.execute(sql)
        self.connection.commit()
    
    def testSQL(self, playlist):
        sql = "insert into PLAYLIST values (\'" + str(playlist.playlist_title) + "\', \'" + str(playlist.total_playlist_tracks) +  "\', \'" + str(playlist.playlist_id) + "\', \'" + str(playlist.account_id) + "\')"
        print(sql)
        delete = "delete from PLAYLIST where playlist_id='" + str(playlist.playlist_id) + "'"
        print(delete)
        update = str("update PLAYLIST set playlist_title=\'" + str(playlist.playlist_title) + "\', total_playlist_tracks=\'" + str(playlist.total_playlist_tracks) +  "\', playlist_id=\'" + str(playlist.playlist_id) +  "\', account_id=\'" + str(playlist.account_id) + "\' where playlist_id='" + str(playlist.playlist_id) + "'")
        print(update)
    
    def getPlaylists(self,sp,userid):
        playlists = sp.current_user_playlists()

        for pl in playlists['items']:
            playlist_id = pl['id']
            playlist_title = pl['name']
            total_playlist_tracks = pl['tracks']['total']
            account_id = userid
            playlist = Playlist(playlist_title, total_playlist_tracks, playlist_id, account_id)

            logging.debug('GET_PLAYLISTS: CALLING SELECT_BY_ID')
            existing_playlist = self.selectByPlaylistId(playlist_id)
            if existing_playlist is None:
                self.insert(playlist)

    def getPlaylistsSpecial(self,sp,userid):
        playlists = sp.current_user_playlists()
        playlistsReturn = []

        for pl in playlists['items']:
            playlist_id = pl['id']
            playlist_title = pl['name']
            total_playlist_tracks = pl['tracks']['total']
            account_id = userid
            playlist = Playlist(playlist_title, total_playlist_tracks, playlist_id, account_id)

            if (playlist_title == 'This Vibe') or (playlist_title == 'Private') or (playlist_title == 'Lil Country') or (playlist_title == 'College Girl'):
                existing_playlist = self.selectByPlaylistId(playlist_id)
                if existing_playlist is None:
                    self.insert(playlist)
                    playlistsReturn.append(playlist_id)
        return playlistsReturn

    # def getPlaylistsForUser(self,sp,userid):
    #     playlists = sp.current_user_playlists()
    #     result= []
    #     for pl in playlists['items']:
    #         playlist_id = pl['id']
    #         playlist_title = pl['name']
    #         total_playlist_tracks = pl['tracks']['total']
    #         account_id = userid
    #         playlist = Playlist(playlist_title, total_playlist_tracks, playlist_id, account_id)

    #         result.append(playlist)
    #     return result
    
    def getPlaylistsForUser(self, playlists):
        result = []
        for playlist in playlists:
            playlist_info = {
                'playlist_title': playlist.playlist_title,
                'total_playlist_tracks': playlist.total_playlist_tracks,
                'playlist_id': playlist.playlist_id,
                'account_id': playlist.account_id}
            result.append(playlist_info)
        return result

    def testPlaylistId(self,id):
        playlists = self.selectAll()
        playlistids = []
        for playlist in playlists:
            playlistid = playlist.playlist_id
            playlistids.append(playlistid)
        
        for pid in playlistids:
            if (pid == id):
                return False
        
        return True

    # def updateNumber(self, playlistid):
    #     playlist = self.selectByPlaylistId(playlistid)
    #     number = int(playlist.total_playlist_tracks)
    #     number =+ 1
    #     newNum = str(number)
    #     new_playlist_number = Playlist(playlist.playlist_title,newNum,playlist.playlist_id,playlist.account_id)
    #     self.update(new_playlist_number)

    def updateNumber(self, playlistid):
        playlist = self.selectByPlaylistId(playlistid)
        number = int(playlist.total_playlist_tracks)
        number =number + 1
        newNum = str(number)
        new_playlist_number = Playlist(playlist.playlist_title,newNum,playlist.playlist_id,playlist.account_id)
        self.update(new_playlist_number)

    def decrementTotal(self, playlistid):
        playlist = self.selectByPlaylistId(playlistid)
        number = int(playlist.total_playlist_tracks)
        number -= 1
        newNum = str(number)
        new_playlist_number = Playlist(playlist.playlist_title,newNum,playlist.playlist_id,playlist.account_id)
        self.update(new_playlist_number)
    


