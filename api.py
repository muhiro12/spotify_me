import os
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import spotipyExtension

USERNAME = str(os.environ.get('SPOTIFY_USER_NAME'))
CLIENT_ID = str(os.environ.get('SPOTIFY_CLIENT_ID'))
CLIENT_SECRET = str(os.environ.get('SPOTIFY_CLIENT_SECRET'))
REDIRECT_URL = 'http://localhost/'

SCOPE = 'user-read-recently-played user-library-modify playlist-read-private user-read-email playlist-modify-public playlist-modify-private user-library-read playlist-read-collaborative user-read-birthdate user-read-playback-state user-read-private app-remote-control user-modify-playback-state user-follow-read user-top-read user-read-currently-playing user-follow-modify streaming'


sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URL, scope=SCOPE, cache_path=".cache-" + USERNAME)
token_info = sp_oauth.get_cached_token()
if not token_info:
	code = os.environ.get('SPOTIFY_AUTHORIZATION_CODE')
	token_info = sp_oauth.get_access_token(code)
token = token_info['access_token']

sp = spotipy.Spotify(token)


def fetchPlaylist(name):
	print('[LOG] fetchPlaylist() was called.')
	id = ''
	results = sp.current_user_playlists()
	for item in results['items']:
		if item['name'] == name:
			id = item['id']
	return id


def updateMyBest():
	print('[LOG] updateMyBest() was called.')
	nameList = []
	idList = []
	results = sp.current_user_top_tracks(limit = 50, time_range = 'medium_term')
	for item in results['items']:
		nameList.append(item['name'])
		idList.append(item['id'])
	if idList != []:
		sp.user_playlist_replace_tracks(USERNAME, fetchPlaylist('#00_Best'), idList)
	return nameList


def updateTop20():
	print('[LOG] updateTop20() was called.')
	nameList = []
	idList = []
	results = sp.current_user_top_tracks(limit = 20, time_range = 'short_term')
	for item in results['items']:
		nameList.append(item['name'])
		idList.append(item['id'])
	if idList != []:
		sp.user_playlist_replace_tracks(USERNAME, fetchPlaylist('#01_Top20'), idList)
	return nameList


def updateRecent():
	print('[LOG] updateRecent() was called.')
	results = sp.current_user_recently_played()
	nameList = []
	idList = []
	for item in results['items']:
		nameList.append(item['track']['name'])
		idList.append(item['track']['id'])
	if idList != []:
		sp.user_playlist_replace_tracks(USERNAME, fetchPlaylist('#02_Recent'), idList)
	return nameList
