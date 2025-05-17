from flask import Flask, redirect, request, session, url_for, render_template, abort, jsonify
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from spotipy.cache_handler import FlaskSessionCacheHandler
import os
import sys
import spotipy
import logging
import random
import string
import requests
from accountdao import AccountDAO
from account import Account
from track import Track
from trackdao import TrackDAO
from album import Album
from albumdao import AlbumDAO
from playlist import Playlist
from playlistdao import PlaylistDAO
from tap import Tap
from tapdao import TapDAO
from tal import Tal
from taldao import TalDAO


FORMAT = "[%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

app = Flask(__name__)

client_id = '6a2***********************'
client_secret = 'b33**********************************'
redirect_uri = 'https://collectparking-spoonfinal-8000.codio.io/callback'
scope = 'user-read-private user-read-email app-remote-control streaming user-modify-playback-state streaming playlist-read-private playlist-modify-private user-top-read user-library-read user-read-email user-modify-playback-state user-read-playback-state user-read-currently-playing user-read-private' 

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(client_id = client_id, client_secret = client_secret ,redirect_uri = redirect_uri, scope = scope, cache_handler = cache_handler, show_dialog = True)

sp = spotipy.Spotify(auth_manager=sp_oauth)

def is_valid_token():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    #cow
    not_valid = is_valid_token()
    if not_valid:
        return not_valid
    
    return redirect(url_for('homepage'))#callback

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    #rawr
    session.clear()
    return login()

@app.route('/index', methods=['GET', 'POST'])
def index():
    access_token = session['access_token']
    return render_template('index.html', **locals())

# @app.route('/store_access_token', methods=['POST'])
# def store_access_token():
#     access_token = request.form.get('access_token')
#     session['access_token'] = access_token
#     print('ACCESS TOKEN FROM STORE ACCESS TOKEN:', access_token)
#     return 'Access token was stored in the session'

# callback works
@app.route('/callback', methods=['GET', 'POST'])
def callback():
    #cat

    token_info = sp_oauth.get_access_token(request.args['code'])
    access_token = token_info['access_token']
    logging.debug("Access Token in Callback: "+str(access_token))
    session['access_token'] = access_token
    sp = spotipy.Spotify(auth=access_token)
    user_info = sp.current_user()

    email = user_info['email']  
    username = user_info['display_name']
    userid = user_info['id']

    accountdao = AccountDAO()
    if accountdao.selectById(userid) is None:
        create_account = accountdao.getUser(email, username, userid) # adds user to db
        playlistdao = PlaylistDAO()
        # playlistdao.getPlaylists(sp,userid) # populates playlist table and gets a list of playlist ids
        playlists = playlistdao.getPlaylistsSpecial(sp,userid)
        album_dao = AlbumDAO()
        album_dao.getAlbums(sp,userid) # populates album table
        taldao = TalDAO()
        taldao.firstInserts(sp,userid) # populates tal table
        not_valid = is_valid_token()
        if not_valid:
            return not_valid
        tapdao = TapDAO()
        # tapdao.firstInserts(sp,userid) # populates tap table
        tapdao.firstInsertsSpecial(sp,userid,playlists)

    current_account = accountdao.getUser(email, username, userid)
    session['userid'] = userid 
    # return redirect(url_for('index'))#if you chnage this redirect to index, you get the working example
    # return render_template('login.html', **locals())
    return redirect(url_for('homepage'))

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    #cheetah
    full_url = request.url
    logging.debug("FULL_URL: " + str(full_url))
    return is_valid_token() or render_template('home.html', **locals())


@app.route('/get_playlist', methods=['GET', 'POST'])
def get_playlist():
    #crocodile
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    user_dao = AccountDAO()
    user = user_dao.selectById(userid)
    username = user.username

    playlist_dao = PlaylistDAO()
    playlists = playlist_dao.selectByUserId(userid)
    return render_template('playlists.html', **locals())

@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    #crocodile
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    if ('addplaylist' in request.form):
        playlist_name = request.form['playlistname']
        playlistid = generate_random_string()
        dao = PlaylistDAO()
        boolean = dao.testPlaylistId(playlistid)
        if boolean is False:
            playlistid = generate_random_string()
        new_playlist = Playlist(playlist_name,'0',playlistid,userid)
        dao.insert(new_playlist)
        return get_playlist()
    else:
        return get_playlist()

# view playlist works
@app.route('/view_playlist', methods=['GET', 'POST'])
def view_playlist():
    #chicken
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    if ('view' in request.form):
        playlistid = request.form['view_playlist']
        logging.debug("Playlist id: "+playlistid)
        dao = TapDAO()
        playlist_tracks = dao.getPlaylistTracks(sp, playlistid)
        # session['playlist_tracks'] = playlist_tracks
        # countArray = []
        # count = 0;
        # for number in playlist_tracks:
        #     countArray.append(count)
        # logging.debug('countArray: ' + countArray)
        session['currentPlaylistId'] = playlistid
        
        return render_template('viewplaylist.html', **locals())
    else:
        return get_playlist()

@app.route('/delete_playlist', methods=['GET', 'POST'])
def delete_playlist():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')
    
    if('delete' in request.form):
        playlistid = request.form['delete_playlist']
        tapdao = TapDAO()
        tapdao.deleteByTapPlaylistId(playlistid)
        playlistdao = PlaylistDAO()
        playlistdao.delete(playlistid)
        return get_playlist()
    else:
        return get_playlist()

@app.route('/play_song', methods=['GET', 'POST'])
def play_song():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')
    access_token = session['access_token']

    if('play' in request.form):
        trackid = request.form['play_song']
        track_info = sp.track(trackid)
        logging.debug("CURRENT TRACK NAME: " + str(track_info['name']))
        playlistid = session['currentPlaylistId']
        dao = TapDAO()
        trackids = dao.selectByTapPlaylistId(playlistid)

        # playlist_tracks = session['playlist_tracks']
        # preview_url = track_info['preview_url']
        # string_length = len(preview_url)
        # new_preview_url = preview_url[6:]
        tracknames = []
        for tid in trackids:
            track_info = sp.track(tid)
            tracknames.append(track_info['name'])

    return render_template('playaudio.html', **locals())

@app.route('/delete_track', methods=['GET', 'POST'])
def delete_track():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    
    
    if('delete' in request.form):
        logging.debug("DOES DELETE TRACK HIT?????????")
        trackid = request.form['delete_track']
        logging.debug("DELETED TRACK " + str(trackid))
        playlistid = session['currentPlaylistId']
        tapdao = TapDAO()
        tapdao.delete(trackid, userid, playlistid)
        playlistdao = PlaylistDAO()
        playlistdao.decrementTotal(playlistid)
        return get_playlist()
    else:
        return get_playlist()

@app.route('/library', methods=['GET', 'POST'])
def library():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid
    
    userid = session.get('userid')
    access_token = session['access_token']
    
    dao = TapDAO()
    tracks = dao.getTotalTracks(sp, userid)
    # artists = [{'name': artist['name'], 'id': artist['id']} for artist in tracks['artists']]

    return render_template('library.html', **locals())
 
#all of the album functions works
@app.route('/get_album', methods=['GET', 'POST'])
def get_album():
    #crocodile
    
    not_valid = is_valid_token()
    if not_valid:
        return not_valid
    
    userid = session.get('userid')
    dao = AlbumDAO()
    albumIds = dao.selectByUserId(userid)
    logging.debug("Album ids: " + str(albumIds))

    albums = []
    for albumId in albumIds:
        album = dao.getAlbumById(sp, albumId.album_id)
        album_info = dao.getAlbumsFromAlbumId(album, albumId.album_id, userid)
        if album_info:
           albums.append(album_info)

    access_token = session.get('access_token')
    logging.debug('ACCESS TOKEN IN get_album METHOD: ', access_token)
    return render_template('viewalbums.html', albums = albums, get_album_image=get_album_image, access_token=access_token)

@app.route('/view_album_songs', methods=['GET', 'POST'])
def view_album_songs():
    #chicken
    not_valid = is_valid_token()
    if not_valid:
        return not_valid
    
    access_token = session['access_token']

    if ('view' in request.form):
        albumid = request.form['view_album_songs']
        album_tracks = sp.album_tracks(albumid)

    return render_template('view_album_songs.html', album=album_tracks['items'], **locals())

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    #cockatoo
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    token_info = cache_handler.get_cached_token()
    if not token_info:
        return "No Token Found"

    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_user = sp.current_user()
    return current_user

# search song works and is all good
@app.route('/search_song', methods=['GET', 'POST'])
def search_song():
    #chipmunk
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    query = request.args.get('query')

    results = sp.search(q=query, type='track')
    tracks = results['tracks']['items']

    if not tracks:
        return "No tracks found."

    access_token = session['access_token']
    # for track in tracks:
    #     track_id = track['id']
    #     track_info = sp.track(track_id)
    #     track['duration_ms'] = track_info['duration_ms']

    return render_template('searchsong.html', **locals())

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    if ('add' in request.form):
        trackid = request.form['add_song']
        session['trackid'] = trackid
        playlist_dao = PlaylistDAO()
        playlists = playlist_dao.selectByUserId(userid)
        return render_template('addsong.html', **locals())
    elif ('add_to_playlist' in request.form):
        trackid = session['trackid']
        playlistid = request.form['playlistidadd']
        
        playlistdao = PlaylistDAO()
        dao = TapDAO()
        if (dao.selectByTrackIdAndPlaylistId(trackid,playlistid,userid) is None):
            tap = Tap(trackid,userid,playlistid)
            dao.insert(tap)
            playlistdao.updateNumber(playlistid)
            return get_playlist()
        else:
            return get_playlist()
    else:
        return library()

# liked songs works
@app.route('/liked_songs', methods=['GET', 'POST'])
def liked_songs():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')
    access_token = session['access_token']

    dao = TalDAO()
    liked_tracks = dao.getLikedTracks(sp,userid)

    return render_template('likedsongs.html', **locals())


@app.route('/add_liked_song', methods=['GET', 'POST'])
def add_liked_song():

    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    if ('like' in request.form):
        trackid = request.form['add_liked_song']
        taldao = TalDAO()
        if (taldao.selectByTrackId(trackid) is None):
            taldao.insert(trackid, userid)
            return liked_songs()
        else:
            return liked_songs()
    else:
        return liked_songs()

@app.route('/delete_liked_song', methods=['GET', 'POST'])
def delete_liked_song():
    not_valid = is_valid_token()
    if not_valid:
        return not_valid

    userid = session.get('userid')

    if ('delete' in request.form):
        trackid = request.form['delete_liked_song']
        taldao = TalDAO()
        taldao.delete(trackid, userid)
        return liked_songs()
    else:
        return liked_songs()

def generate_random_string():
    # Define the pool of characters to choose from
    characters = string.ascii_letters + string.digits  # Letters (both cases) and digits

    # Generate the random string by selecting characters randomly from the pool
    random_string = ''.join(random.choice(characters) for _ in range(22))

    return random_string

def get_album_image(album_id):
    album_data = sp.album(album_id)

    if 'images' in album_data and len(album_data['images']) > 0:
        return album_data['images'][0]['url']

def get_playlist_image(playlist_id):
    playlist_data = sp.playlist(playlist_id)

    if 'images' in playlist_data and len(playlist_data['images']) > 0:
        return playlist_data['images'][0]['url']

# @app.route('/get_access_token', methods=['GET'])
# def get_access_token():
#     access_token = session.get('access_token')

#     return jsonify({'access_token': access_token})

# @app.route('/check_access_token_validity', methods=['GET'])
# def check_access_token_validity():
#     # if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#     auth_url = sp_oauth.get_authorize_url()
#     logging.debug(auth_url)
#     return jsonify({'valid': True, 'auth_url': auth_url})

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)


# sample playlistid - 73Hx17RKj5iMosDJiUzVnl

# Layout:
# User logs in and we check if the user is in our database
    # if not in database - we add them, and add all their playlists and tracks to the databases
    # else continue onto home page and the other features listed down below

# What can the user do? (def add to this)
    # Search a song - maybe add to the playlist? This would then add the song to both the playlist and track database
        # If they want to add to a playlist, take the ID and put into a session...? and then
        # redirect to a page that lists all the playlists and has a button to choose then 
        # take the id and add to that certain playlist
    # View Playlists - Will have to see what specific modifications they can do, but make sure databases keep up
    # Look at library - This is where we get all the tracks associated with a certain user and put them alphabetically
    # Click a Song - this will play the song
    # Logout

# Database Tables
    # Account  
        # email, username, id
    # Album
        # Album id (PK), account id (FK)
    # Playlist
        # Title, total tracks, playlist id, account id (FK)
    # TAP
        # track id, playlist id, account id
    # TAL
        # track id, account id
        # Primary Key is track id + account id


# I will make the track ones rn and work on album rn too, i think album and playlists are working correctly, just check first
# Also gonna work on code for like 6-8 hrs tmr so be aware
# Quick q - we need to import SpotifyOAuth in dao if we call sp correct?- no, just call it from the testingcode, i did it with the album and playlist daos

# To Do Tmr:
    # Make sure DAOs are all good
    # Think of format for html and stuff
    # Write the methods and stuff to insert a new user into the db and all their user_info- i thik the callback creates new user in the account db, just double check to make sure i did that right

    # HTML format (change if incorrect)
        # home.html -- is the main page and still trynna figure out what that will have except for all the navigations
        # library.html -- will list all the songs that a user has from the TAL table 
        # playlists.html -- will list all playlists from the Playlist table (using account id) (could also use TAP table) 
                            # and then grab all tracks from the TAP table given the playlist and account ids
                            # and then render to the viewplaylist.html.
                            # Will also be able to add a playlist and maybe this could be a text box with the button 
                            # add below that becuase we only ask for the title. This gets added to relevant tables
                            # Issues - getting a unique playlistID
                            # Relevant Tables - Playlist, maybe TAP
        # viewplaylist.html -- This will list all the tracks in that certain playlist and will allow
                                # one to view the album associated with that track by using the album id
                                # in the track table. Renders to viewalbums.html (have to change)
        # searchsong.html -- will search a song and this will give the option to add that song to a playlist
                            # this will render to a template called addsong.html (need to add) that lists 
                            # all your playlists given the account id in the Playlist table and you select one
                            # this will then add it and render you to the viewplaylist.html where you will see the new
                            # song added to your playlist (adds to the database and all its relevant tables)
                            # Relevant Tables - Track table, TAP, TAL
    
    # Other
        # likedTracks will be a separate playlist within the playlist.html (each user will have one)
