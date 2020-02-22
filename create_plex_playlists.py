"""
Script to iterate over all favorite tracks for a list of artists and
create playlists of favorites
"""

import os, logging
from plexapi.myplex import MyPlexAccount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    PLEX_USER = os.getenv("PLEX_USER")
    PLEX_SERVER = os.getenv("PLEX_SERVER")
    PLEX_PASSWORD = os.getenv("PLEX_PASSWORD")

    logger.debug("Authenticating to Plex server...")
    account = MyPlexAccount(PLEX_USER, PLEX_PASSWORD)
    plex = account.resource(PLEX_SERVER).connect()

    grunge_artists = ["Metallica", "Pearl Jam", "Alice in Chains", "Nirvana", "Tool", "Soundgarden", "Silverchair", "Bush", "Candlebox", "Stone Temple Pilots"]
    create_playlist(plex, "Grunge", grunge_artists)

"""
Create a playlist from a list of artists
"""
def create_playlist(plex, playlist_title, artists):
    logger.info(f"Creating playlist {playlist_title}")
    favorites = [(artist_name, get_favorites_for_artist(artist_name, plex)) for artist_name in artists]

    for artist, tracks in favorites:
        logger.info(f"name: {artist} ({len(tracks)})")

    playlist = [playlist for playlist in plex.playlists() if playlist.title == playlist_title]
    if playlist:
        playlist[0].delete()
    
    plex.createPlaylist(playlist_title, tracks, "audio")
    logger.info("Playlist created")
        
"""
Get favorited tracks from Plex for an artist
"""
def get_favorites_for_artist(artist_name, plex):
    artist = plex.library.section('Music').get(artist_name)
    logger.debug(f"Processing tracks for {artist}...")
    
    tracks = [track for track in artist.tracks()]
    return [track for track in tracks if track.userRating == 10.0]

if __name__ == "__main__":
    main() 
