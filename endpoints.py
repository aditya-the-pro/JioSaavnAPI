import urllib.parse


def song_search(name):
    return f"https://www.jiosaavn.com/api.php?p=1&_format=json&_marker=0&api_version=4&ctx=wap6dot0&n=10&__call=search.getResults&q={name}"


def song_links(song_id):
    return f"https://www.jiosaavn.com/api.php?__call=song.getDetails&pids={song_id}&api_version=4&_format=json&_marker=0&ctx=web6dot0"


def auth_url(link):
    link = urllib.parse.quote(link)
    return f"https://www.jiosaavn.com/api.php?__call=song.generateAuthToken&url={link}&bitrate=128&api_version=4&_format=json&ctx=web6dot0&_marker=0"



def ablum_url(id):
    return f"https://www.jiosaavn.com/api.php?__call=autocomplete.get&_format=json&_marker=0&cc=in&includeMetaTags=1&query={id}"



def album_by_id(album_id:int):
    return f"https://www.jiosaavn.com/api.php?__call=content.getAlbumDetails&_format=json&cc=in&_marker=0%3F_marker=0&albumid={album_id}"

def lyrics_url(id):
    return f"https://www.jiosaavn.com/api.php?__call=lyrics.getLyrics&lyrics_id={id}&ctx=wap6dot0&api_version=4&_format=json&_marker=0"



def top_search():
    return f"https://www.jiosaavn.com/api.php?__call=content.getTopSearches&ctx=wap6dot0&api_version=4&_format=json&_marker=0"



def get_trending():
    return f"https://www.jiosaavn.com/api.php?__call=content.getTrending&api_version=4&_format=json&_marker=0&ctx=wap6dot0&entity_type=album&entity_language=punjabi"


def get_home_page():
    return f"https://www.jiosaavn.com/api.php?__call=content.getHomepageData"


def playlist(playlist_id):
    return f"https://www.jiosaavn.com/api.php?__call=playlist.getDetails&_format=json&cc=in&_marker=0%3F_marker%3D0&listid={playlist_id}"