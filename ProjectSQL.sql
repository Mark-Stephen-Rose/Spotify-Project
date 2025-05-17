
CREATE TABLE ALBUM (album_id varchar(255), account_id varchar(255), 
FOREIGN KEY (account_id) REFERENCES ACCOUNT(id), PRIMARY KEY (album_id,account_id))

CREATE TABLE PLAYLIST (playlist_title varchar(255), total_playlist_tracks varchar(255),
playlist_id varchar(255) PRIMARY KEY, account_id varchar(255),
FOREIGN KEY (account_id) REFERENCES ACCOUNT(id))

CREATE TABLE TAP (track_id varchar(255), account_id varchar(255), 
FOREIGN KEY (account_id) REFERENCES ACCOUNT(id), playlist_id varchar(255) PRIMARY KEY,
FOREIGN KEY (playlist_id) REFERENCES PLAYLIST(playlist_id))

CREATE TABLE TAL (track_id varchar(255), account_id varchar(255),
FOREIGN KEY (account_id) REFERENCES ACCOUNT(id), PRIMARY KEY (track_id,account_id))

SELECT * FROM ACCOUNT

SELECT * FROM PLAYLIST 

SELECT * FROM ALBUM 

SELECT * FROM TAP 

SELECT * FROM TAL



