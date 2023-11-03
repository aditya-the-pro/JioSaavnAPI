import httpx
import endpoints


def jsonDataMaker(rawJson):
    k = {
        "id": rawJson["id"],
        "song": rawJson["title"],
        "album": rawJson["more_info"]["album"],
        "year": rawJson["year"],
        "primary_artist": artistHelper(
            rawJson["more_info"]["artistMap"]["primary_artists"], "primary"
        ),
        "singers": artistHelper(rawJson["more_info"]["artistMap"]["artists"], "singer"),
        "imgs": imgHelper(rawJson["image"]),
        "duration": durationHelper(int(rawJson["more_info"]["duration"])),
        "label": rawJson["more_info"]["label"],
        "album_id": rawJson["more_info"]["album_id"],
        "language": rawJson["language"],
        "copyright_text": rawJson["more_info"]["copyright_text"],
        "has_lyrics": rawJson["more_info"]["has_lyrics"],
        "links": getDirectURL(rawJson["more_info"]["encrypted_media_url"]),
        "perma_url": rawJson["perma_url"],
        "album_url": rawJson["more_info"]["album_url"],
        "release_date": rawJson["more_info"]["release_date"],
    }
    return k


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


def durationHelper(seconds: int):
    (mins,secs) = divmod(seconds, 60)
    # ? : check the seconds for wildcard or tenth place zero
    secs = f"0{secs}" if secs in range(0,9) else secs
    return f"{mins}:{secs}"


def getDirectURL(link):
    t = httpx.get(endpoints.auth_url(link)).json()

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


def resultRender(data: dict):
    if len(data) == 0:
        return {"msg": "no song found"}
    else:
        t = []

        for x in data:
            b = {
                "id": x["id"],
                "title": x["title"],
                "imgs": imgHelper(x["image"]),
                "album": x["more_info"]["album"],
                "description": x["subtitle"],
                "more_info": {
                    "vlink": x["more_info"].get("vlink"),
                    "singers": artistHelper(
                        x["more_info"]["artistMap"]["artists"], "singer"
                    ),
                    "language": x["language"],
                    "album_id": x["more_info"]["album_id"],
                },
                "perma_url": x["perma_url"],
            }

            t.append(b)

        return t


def lyricsHelper(json):
    if not "lyrics" in json:
        return {"msg": "lyrics not found"}
    else:
        return {"lyrics": json["lyrics"]}


def albumSearchHelper(json, base_url):
    # return json
    if len(json["albums"]["data"]) == 0:
        return {"msg": "no album found"}
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



def radio_song_helper(song_dict:dict):
    # * : here make the full songs dict and do not append the station id again the response
    
    relayer_dict = []
    for x in song_dict:
        if x != 'stationid':
            relayer_dict.append(song_dict[x]['song'])
            
    song_dict = []
    for x in relayer_dict:
        song_dict.append(jsonDataMaker(x))
    return song_dict