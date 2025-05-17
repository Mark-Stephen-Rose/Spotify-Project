import cx_Oracle
from tap import Tap
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class TapDAO:
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

    def rowToTap(self,row):
        tap = Tap(row[0],row[1],row[2])
        return tap

    def tapToRow(self,tap):
        row = dict(track_id=tap.track_id, account_id=tap.account_id, playlist_id=tap.playlist_id)
        return row

    def insert(self,tap):
        sql = "insert into TAP values (\'" + str(tap.track_id) + "\', \'" + str(tap.account_id) +  "\', \'" + str(tap.playlist_id) + "\')"
        self.cursor.execute(sql)
        self.connection.commit()

    def delete(self, trackid, userid, playlistid):
        sql = "delete from TAP where track_id='" + str(trackid) + "' AND account_id='" + str(userid) + "' AND playlist_id='" + str(playlistid) + "'"
        self.cursor.execute(sql)
        self.connection.commit()
    
    def deleteByTapTrackId(self,tap):
        sql = "delete from TAP where track_id='" + str(tap.track_id) + "'"
        self.cursor.execute(sql)
        self.connection.commit()
    
    def deleteByTapAccountId(self,tap):
        sql = "delete from TAP where account_id='" + str(tap.account_id) + "'"
        self.cursor.execute(sql)
        self.connection.commit()
    
    def deleteByTapPlaylistId(self,id):
        sql = "delete from TAP where playlist_id='" + str(id) + "'"
        self.cursor.execute(sql)
        self.connection.commit()

    def deleteAll(self):
        sql = "delete from TAP"
        self.cursor.execute(sql)
        self.connection.commit()

    def selectAll(self):
        sql = "select * from TAP"
        self.cursor.execute(sql)
        tap=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            tapItem = self.rowToTap(row)
            tap.append(tapItem)
        return tap

    def selectByTapTrackId(self,tap):
        sql = "select * from TAP where track_id='" + str(tap.track_id) + "'"
        self.cursor.execute(sql)
        tap=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            tapItem = self.rowToTap(row)
            tap.append(tapItem.track_id)
        return tap
    
    def selectByTapAccountId(self,tap):
        sql = "select * from TAP where account_id='" + str(tap.account_id) + "'"
        self.cursor.execute(sql)
        tap=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            tapItem = self.rowToTap(row)
            tap.append(tapItem.track_id)
        return tap

    def selectByTapPlaylistId(self,id):
        sql = "select * from TAP where playlist_id='" + str(id) + "'"
        self.cursor.execute(sql)
        tap=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            tapItem = self.rowToTap(row)
            tap.append(tapItem.track_id)
        return tap

    def selectByTrackIdAndPlaylistId(self, trackid, playlistid, userid):
        sql = "select * from TAP where track_id='" + str(trackid) + "' AND account_id='" + str(userid) + "' AND playlist_id='" + str(playlistid) + "'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row!= None:
            tap = self.rowToTap(row)
            return tap
        return None
    
    def testSQL(self, tap):
        insert = "insert into TAP values (\'" + str(tap.track_id) + "\', \'" + str(tap.account_id) +  "\', \'" + str(tap.playlist_id) + "\')"
        print(insert)
        delete = "delete from TAP where track_id='" + str(tap.track_id) + "' AND account_id='" + str(tap.account_id) + "' AND playlist_id='" + str(tap.playlist_id) + "'"
        print(delete)
        trackid = "select * from TAP where track_id='" + str(tap.track_id) + "'"
        print(trackid)
        accountid = "select * from TAP where account_id='" + str(tap.account_id) + "'"
        print(accountid)
        playlistid = "select * from TAP where playlist_id='" + str(tap.playlist_id) + "'"
        print(playlistid)

    def getAllPlaylists(self, sp, userid):
        offset = 0
        limit = 50
        all_playlists = []

        while True:
            playlists = sp.user_playlists(userid, limit=limit, offset=offset)
            all_playlists.extend(playlists['items'])
            
            # Check if there are more playlists
            if playlists['total'] <= offset + limit:
                break
            
            offset += limit
    
        return all_playlists

    def getTracks(self, sp, playlist_id):
        tracks = []
        offset = 0
        limit = 100  # Maximum limit for playlist tracks endpoint

        while True:
            playlist_response = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            tracks.extend(playlist_response['items'])

            # Check if there are more tracks
            if not playlist_response['next']:
                break

            offset += limit

        return tracks

    def firstInserts(self, sp, userid):
        playlists = self.getAllPlaylists(sp, userid)
        logging.debug('Userid: ' + userid)
        for pl in playlists:
            playlist_id = pl['id']
            tracks = self.getTracks(sp, playlist_id)
            logging.debug('Playlist_id: ' + playlist_id)
            logging.debug('Userid: ' + userid)

            for track in tracks:
                track_info = track['track']
                track_id = track_info['id']
                tap = Tap(track_id,userid,playlist_id)
                self.insert(tap)

    def firstInsertsSpecial(self, sp, userid, playlists):
        for playlistid in playlists:
            tracks = self.getTracks(sp, playlistid)

            for track in tracks:
                track_info = track['track']
                track_id = track_info['id']
                tap = Tap(track_id,userid,playlistid)
                self.insert(tap)

    def distinctTracks(self, userid):
        sql = "select distinct track_id from TAP where account_id='" + str(userid) + "'"
        self.cursor.execute(sql)
        tap=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            tap.append(row[0])
        return tap

    def getPlaylistTracks(self, sp, playlistid):
        trackids = self.selectByTapPlaylistId(playlistid)
        tracks = []
        for trackid in trackids:
            track = sp.track(trackid)
            tracks.append(track)
        return tracks

    def getTotalTracks(self,sp,userid):
        trackids = self.distinctTracks(userid)
        tracks = []
        for trackid in trackids:
            #logging.debug("track id: "+trackid)
            track = sp.track(trackid)
            tracks.append(track)
        return tracks


    


