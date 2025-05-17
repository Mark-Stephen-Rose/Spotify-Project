import cx_Oracle
from tal import Tal
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

class TalDAO:
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

    def rowToTal(self,row):
        tal = Tal(row[0],row[1])
        return tal

    def talToRow(self,tal):
        row = dict(track_id=tal.track_id, account_id=tal.account_id)
        return row

    def insert(self,trackid, userid):
        sql = "insert into TAL values (\'" + str(trackid) + "\', \'" + str(userid) + "\')"
        self.cursor.execute(sql)
        self.connection.commit()

    def insert1(self,tal):
        sql = "insert into TAL values (\'" + str(tal.track_id) + "\', \'" + str(tal.account_id) + "\')"
        self.cursor.execute(sql)
        self.connection.commit()

    def delete(self,trackid, userid):
        sql = "delete from TAL where track_id='" + str(trackid) + "' AND account_id='" + str(userid) + "'"
        self.cursor.execute(sql)
        self.connection.commit()

    def deleteAll(self):
        sql = "delete from TAL"
        self.cursor.execute(sql)
        self.connection.commit()

    def selectAll(self):
        sql = "select * from TAL"
        self.cursor.execute(sql)
        tal=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            talItem = self.rowToTal(row)
            tal.append(talItem)
        return tal

    def selectByAccountId(self,id):
        sql = "select * from TAL where account_id='" + str(id) + "'"
        self.cursor.execute(sql)
        tal=[]
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            talItem = self.rowToTal(row)
            tal.append(talItem.track_id)
        return tal

    def selectByTrackId(self,id):
        sql = "select * from TAL where track_id='" + str(id) + "'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row!= None:
            tal = self.rowToTal(row)
            return tal
        return None
    
    def testSQL(self, tal):
        insert = "insert into TAL values (\'" + str(tal.track_id) + "\', \'" + str(tal.account_id) +  "\', \'" + str(tal.liked_tracks) + "\')"
        print(insert)
        delete = "delete from TAL where account_id='" + str(tal.account_id) + "'"
        print(delete)
        accountid = "select * from TAL where account_id='" + str(tal.account_id) + "'"
        print(accountid)

    def getAllTracks(self, sp, userid):
        offset = 0
        limit = 50
        all_tracks = []

        while True:
            tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
            all_tracks.extend(tracks['items'])
            
            # Check if there are more tracks
            if not tracks['next']:
                break
            
            offset += limit
    
        return all_tracks
    
    def firstInserts(self, sp, userid):
        tracks = self.getAllTracks(sp,userid)

        for track in tracks:
            track_info = track['track']
            trackid = track_info['id']
            tal = Tal(trackid,userid)
            self.insert1(tal)

    def getLikedTracks(self, sp, userid):
        trackids = self.selectByAccountId(userid)
        tracks = []
        for trackid in trackids:
            track = sp.track(trackid)
            tracks.append(track)
        return tracks
