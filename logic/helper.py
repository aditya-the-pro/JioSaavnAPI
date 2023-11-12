import httpx
from logic.endpoints import *


# this is the song obj that will be given when called by a song_id
from models.song import Song


# its the short form of the song obj basically before htitting the serve for media_link
from models.search_models.search_entity_song import SearchEntitySong

# the ablum search model
from models.search_models.search_entity_album import SearchEntityAlbum

# its the std Album obj response that will be given out when called by a specifc album id
from models.album import Album


def imgHelper(link):
    # ? : check the img size if it is 50x50 or 150x150
    size = "50x50" if "50x50" in link else "150x150" if "150x150" in link else "500x500"
    match size:
        case "50x50":
            links = {
                "50x50": link,
                "150x150": link.replace(size, "150x150"),
                "500x500": link.replace(size, "500x500"),
            }
        case "150x150":
            links = {
                "50x50": link.replace(size, "50x50"),
                "150x150": link,
                "500x500": link.replace(size, "500x500"),
            }
        case "500x500":
            links = {
                "50x50": link.replace(size, "50x50"),
                "150x150": link.replace(size, "150x150"),
                "500x500": link,
            }
        case _:
            # ! : they improved their img quality i doubt
            links = {"unknown img size found"}

    return links


def duration_helper(seconds: int):
    (mins, secs) = divmod(seconds, 60)
    # ? : check the seconds for wildcard or tenth place zero
    secs = f"0{secs}" if secs in range(0, 10) else secs
    return f"{mins}:{secs}"


def get_direct_links(link):
    t = httpx.get(auth_url(link)).json()

    if "auth_url" in t:
        t = t["auth_url"].rsplit("?")
        t = t[0]
        t = t.replace("https://ac.cf.saavncdn.com/", "https://aac.saavncdn.com/")

        t = {
            "96_KBPS": t.replace("_160", "_96"),
            "160_KBPS": t,
            "320_KBPS": t.replace("_160", "_320"),
        }
        return t
    else:
        return {"msg": "error"}


def artistHelper(data, mode="primary" or "singer"):
    t = []
    if mode == "primary":
        if data.__len__() > 0:
            for x in data:
                t.append(x["name"])
            return ", ".join(t)
        else:
            return t
    elif mode == "singer":
        if data.__len__() > 0:
            for x in data:
                if x["role"] == "singer":
                    t.append(x["name"])
            return ", ".join(t)
        else:
            return t
    else:
        return {"msg": "error"}


def albumSearchHelper(json, base_url):
    # return json
    if len(json["albums"]["data"]) == 0:
        return {"detail": "no album found"}
    else:
        t = []
        for x in json["albums"]["data"]:
            t.append(
                {
                    "id": x["id"],
                    "title": x["title"],
                    "img": imgHelper(x["image"]),
                    "music": x["music"],
                    "description": x["description"],
                    "more_info": {
                        "year": x["more_info"]["year"],
                        "language": x["more_info"]["language"],
                    },
                    "url": x["url"],
                    "api_url": {
                        "songs": multiSongList(x["more_info"]["song_pids"], base_url),
                        "album": f"{base_url}album/{x['id']}",
                    },
                }
            )
        return t


def multiSongList(song_ids_str, base_url):
    t = []
    for x in song_ids_str.split(", "):
        t.append(f"{base_url}song/{x}")
    return t


def radio_song_helper(song_dict: dict, base_url: str, use_mins: bool):
    # * : here make the full songs dict and do not append the station id again in the response

    relayer_dict = []
    for x in song_dict:
        if x != "stationid":
            relayer_dict.append(song_dict[x]["song"])

    song_dict = []
    for x in relayer_dict:
        song_dict.append(song_model_helper(x, base_url=base_url, use_mins=use_mins))
    return song_dict


def song_model_helper(song_data, use_mins, base_url):
    return Song(
        id=song_data["id"],
        song=song_data["title"],
        album=song_data["more_info"]["album"],
        year=int(song_data["year"]),
        primary_artists=artistHelper(
            song_data["more_info"]["artistMap"]["primary_artists"], "primary"
        ),
        singers=artistHelper(song_data["more_info"]["artistMap"]["artists"], "singer"),
        imgs=imgHelper(song_data["image"]),
        # if we get the query param to use mins only then we will convert it to mins
        duration=duration_helper(int(song_data["more_info"]["duration"]))
        if use_mins
        else int(song_data["more_info"]["duration"]),
        label=song_data["more_info"]["label"],
        album_id=int(song_data["more_info"]["album_id"]),
        language=song_data["language"],
        copyright_text=song_data["more_info"]["copyright_text"],
        has_lyrics=song_data["more_info"]["has_lyrics"],
        links=get_direct_links(song_data["more_info"]["encrypted_media_url"]),
        perma_url=song_data["perma_url"],
        album_url=song_data["more_info"]["album_url"],
        release_date=song_data["more_info"]["release_date"],
        api_url={
            "album": f"{base_url}album/{song_data['more_info']['album_id']}",
        },
    )


def song_search_helper(data: dict, base_url):
    t = []
    for x in data:
        t.append(
            SearchEntitySong(
                id=x["id"],
                title=x["title"],
                imgs=imgHelper(x["image"]),
                album=x["more_info"]["album"],
                description=x["subtitle"],
                more_info={
                    "vlink": x["more_info"].get("vlink"),
                    "singers": artistHelper(
                        x["more_info"]["artistMap"]["artists"], "singer"
                    ),
                    "language": x["language"],
                    "album_id": int(x["more_info"]["album_id"]),
                },
                perma_url=x["perma_url"],
                api_url={
                    "song_url": f"{base_url}song/{x['id']}",
                    "album_url": f"{base_url}album/{x['more_info']['album_id']}",
                },
            )
        )

    return t


def album_model_helper(data: dict, use_mins, base_url):
    # let me prepare the song list here that will be passed inside album obj
    songs_list = []
    for song_data in data["songs"]:
        songs_list.append(
            Song(
                id=song_data["id"],
                song=song_data["song"],
                album=song_data["album"],
                year=int(song_data["year"]),
                primary_artists=song_data["primary_artists"],
                singers=song_data["singers"],
                imgs=imgHelper(song_data["image"]),
                # if we get the query param to use mins only then we will convert it to mins
                duration=duration_helper(int(song_data["duration"]))
                if use_mins
                else int(song_data["duration"]),
                label=song_data["label"],
                album_id=int(song_data["albumid"]),
                language=song_data["language"],
                copyright_text=song_data["copyright_text"],
                has_lyrics=song_data["has_lyrics"],
                links=get_direct_links(song_data["encrypted_media_url"]),
                perma_url=song_data["perma_url"],
                album_url=song_data["album_url"],
                release_date=song_data["release_date"],
                api_url={
                    "album": f"{base_url}album/{song_data['albumid']}",
                },
            )
        )

    # return data

    return Album(
        title=data["title"],
        name=data["name"],
        year=data["year"],
        release_date=data["release_date"],
        primary_artists=data["primary_artists"],
        # maybe getting null , its okay to be safe here
        primary_artists_id=data.get("primary_artists_id"),
        albumid=data["albumid"],
        perma_url=data["perma_url"],
        imgs=imgHelper(data["image"]),
        songs=songs_list,
    )


def album_search_helper(data: dict, base_url):
    t = []
    for x in data:
        t.append(
            SearchEntityAlbum(
                id=x["id"],
                title=x["title"],
                imgs=imgHelper(x["image"]),
                music=x["subtitle"],
                description=x["header_desc"],
                song_count=x["more_info"]["song_count"],
                more_info={
                    "year": x["year"],
                    "language": x["language"],
                },
                perma_url=x["perma_url"],
                api_url={
                    # "songs": {}, it should be given when we request it by passing id
                    #  ! : maybe bad idea
                    "album": f"{base_url}album/{x['id']}",
                },
            )
        )

    return t
