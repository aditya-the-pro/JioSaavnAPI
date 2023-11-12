import urllib.parse


def search_all_url(query):
    return f"https://www.jiosaavn.com/api.php?__call=autocomplete.get&query={query}&_format=json&_marker=0&ctx=wap6dot0"


def song_search(name):
    return f"https://www.jiosaavn.com/api.php?p=1&_format=json&_marker=0&api_version=4&ctx=wap6dot0&n=10&__call=search.getResults&q={name}"


def song_links(song_id):
    return f"https://www.jiosaavn.com/api.php?__call=song.getDetails&pids={song_id}&api_version=4&_format=json&_marker=0&ctx=web6dot0"


# ? : this func is responsible for giving the correct auth_url to get the songlink
def auth_url(link) -> str:
    link = urllib.parse.quote(link)
    # i dont know what to do at this point did some fuzzing found less bitrate songs
    # going with default bitrate
    bitrate = 128
    return f"https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url={link}&bitrate={bitrate}&api_version=4&_format=json&ctx=web6dot0&_marker=0"


def search_ablum(name):
    return f"https://www.jiosaavn.com/api.php?p=1&q={name}&_format=json&_marker=0&api_version=4&ctx=wap6dot0&n=20&__call=search.getAlbumResults"


def album_by_id(album_id: int):
    return f"https://www.jiosaavn.com/api.php?__call=content.getAlbumDetails&_format=json&cc=in&_marker=0%3F_marker=0&albumid={album_id}"


def lyrics_url(id):
    return f"https://www.jiosaavn.com/api.php?__call=lyrics.getLyrics&lyrics_id={id}&ctx=wap6dot0&api_version=4&_format=json&_marker=0"


def top_search():
    return f"https://www.jiosaavn.com/api.php?__call=content.getTopSearches&ctx=wap6dot0&api_version=4&_format=json&_marker=0"


def get_trending():
    return f"https://www.jiosaavn.com/api.php?__call=content.getTrending&api_version=4&_format=json&_marker=0&ctx=wap6dot0&entity_type=album&entity_language=punjabi"


def get_homepage():
    return f"https://www.jiosaavn.com/api.php?__call=content.getHomepageData"


def playlist(playlist_id):
    return f"https://www.jiosaavn.com/api.php?__call=playlist.getDetails&_format=json&cc=in&_marker=0%3F_marker%3D0&listid={playlist_id}"


def create_radio_station(song_id):
    # basically give the song id to start radio for
    song_id = '["' + urllib.parse.quote(song_id) + '"]'
    return f"https://www.jiosaavn.com/api.php?__call=webradio.createEntityStation&entity_id={song_id}&entity_type=queue&freemium=&shared=&api_version=4&_format=json&_marker=0&ctx=wap6dot0"


def get_songs_from_radio(station_id, num_of_songs):
    # action = "1" if action == "fwd" else "0" if action == "bck" else "1"
    return f"https://www.jiosaavn.com/api.php?__call=webradio.getSong&stationid={station_id}&k={num_of_songs}&next=1&api_version=4&_format=json&_marker=0&ctx=wap6dot0"
