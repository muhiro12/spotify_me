import spotipy

def current_user_recently_played(self, limit=50):
    ''' Get the current user's recently played tracks
    
        Parameters:
            - limit - the number of entities to return
    '''        
    return self._get('me/player/recently-played', limit=limit)

setattr(spotipy.Spotify, 'current_user_recently_played', current_user_recently_played)
