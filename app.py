from flask import *

app = Flask(__name__)

import pyrebase

config = {
    "apiKey": "AIzaSyB7hN8Ya83Xt34nKD1U2K0AtNLQU41q1",
    "authDomain": "spotify-alarm-b61ae.firebaseapp.com",
    "databaseURL": "https://spotify-alarm-b61ae-default-rtdb.firebaseio.com",
    "projectId": "spotify-alarm-b61ae",
    "storageBucket": "spotify-alarm-b61ae.appspot.com",
    "messagingSenderId": "820829797231"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = Flask(__name__)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

cid = "ac699f4f7bf7436380637c9e0720bc67"
secret = "9c14670bdf2042c6a4b0e7463d4eadd2"
scope = "user-read-playback-state " \
        "playlist-modify-public " \
        "playlist-modify-private " \
        "user-top-read " \
        "user-modify-playback-state " \
        "playlist-read-collaborative"

@app.route('/test', methods=['GET'])
def test():
    return "Hello World"

@app.route('/', methods=['GET', 'POST'])
def basic():

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    id = sp.current_user()['id']
    todo = db.child(id).get()
    object = todo.val()
    tokensAdded = False
    to = []
    if object is not None:
        keys = todo.val().keys()
        for key in keys:
            if ":" in key:
                to.append(key)
            else:
                tokensAdded = True
    if not tokensAdded:
        if not request.args.get('access_token'):
            return redirect("http://localhost:8888", code = 302)
        else:
            access_token = request.args.get('access_token')
            refresh_token = request.args.get('refresh_token')
            db.child(id).push({"access_token": access_token, "refresh_token": refresh_token})
    devices = sp.devices()
    deviceNames = []
    deviceIds = []
    deviceTypes = []
    for d in devices['devices']:
        deviceNames.append(d['name'])
        deviceIds.append(d['id'])
        deviceTypes.append(d['type'])
    userPlaylists = {}
    userPlaylistsNames = []
    userPlaylistsIds = []
    currentOffset = 0
    while True:
        userPlaylists = sp.current_user_playlists(limit=50, offset=currentOffset)
        for p in userPlaylists['items']:
            userPlaylistsNames.append(p['name'])
            userPlaylistsIds.append(p['id'])
        if len(userPlaylists['items']) < 50:
            break
        else:
            currentOffset += 50
    if request.method == 'POST':
        if request.form['submit'] == 'add':
#           replace "user" with the user's spotify username that is acquired with api call
            time = request.form['time']
            playlistType = request.form['playlistType']
            period = request.form['timePeriod']
            volume = request.form['volume']
            device = request.form['devices']
            userPlaylistSelection = request.form['playlists']
            duplicate = False
            if to is not None:
                for alarmTime in to:
                    if alarmTime == time:
                        duplicate = True
            if duplicate != True:
                if playlistType == 'recent_favorites':
                    db.child(id).child(time).push(period)
                    db.child(id).child(time).push(volume)
                    db.child(id).child(time).push(device)
                else:
                    db.child(id).child(time).push(userPlaylistSelection)
                    db.child(id).child(time).push(volume)
                    db.child(id).child(time).push(device)
            todo = db.child(id).get()
            object = todo.val()
            keys = todo.val().keys()
            to = []
            if object is not None:
                keys = todo.val().keys()
                to = []
                for key in keys:
                    if ":" in key:
                        to.append(key)
            return render_template('public/userForm.html', t=to, d=duplicate, names=deviceNames, ids=deviceIds, types=deviceTypes, pName=userPlaylistsNames, pId=userPlaylistsIds)
        elif ':' in request.form['submit']:
            for val in to:
                if val == request.form['submit']:
                    db.child(id).child(val).remove()
            todo = db.child(id).get()
            object = todo.val()
            if object is not None:
                keys = todo.val().keys()
                to = []
                for key in keys:
                    if ":" in key:
                        to.append(key)
#        elif request.form['submit'] == 'delete_all':
#            keys = todo.val().keys()
#            if object is not None:
#                for key in to:
#                    db.child(id).remove(key)
#            return render_template('public/userForm.html', names=deviceNames, ids=deviceIds, types=deviceTypes)
        if object is None:
            return render_template('public/userForm.html', names=deviceNames, ids=deviceIds, types=deviceTypes, pName=userPlaylistsNames, pId=userPlaylistsIds)
        return render_template('public/userForm.html', t=to, names=deviceNames, ids=deviceIds, types=deviceTypes, pName=userPlaylistsNames, pId=userPlaylistsIds)
    if object is None:
        return render_template('public/userForm.html', names=deviceNames, ids=deviceIds, types=deviceTypes, pName=userPlaylistsNames, pId=userPlaylistsIds)
    return render_template('public/userForm.html', t=to, names=deviceNames, ids=deviceIds, types=deviceTypes, pName=userPlaylistsNames, pId=userPlaylistsIds)

@app.route('/time')
def get_current_time():
    access_id = request.args.get('access_id')
    email = request.args.get('email')
    return {"access_id":access_id, "email":email}
    
@app.route('/timexx')
def indexhtml():
    return render_template("public/index.html")
