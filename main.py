from fastapi import FastAPI, Request, HTTPException, Depends
import httpx
from logic.endpoints import *
from logic.helper import *

# * INFO : experimental


# TODO : add the playlist, homepage features and more :)

# app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app = FastAPI()
app.title = "JioSaavnAPI"


async def make_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            raise HTTPException(
                status_code=500,
                detail="server ip got banned for api rate limits",
            )
        else:
            raise HTTPException(
                status_code=500, detail="unknown server error go debug it"
            )


def base_url(request: Request):
    return request.base_url._url


@app.get("/")
async def root():
    return {"detail": "Yes, its working fine !"}


@app.get("/search/all/{query}")
async def search_all(query):
    url = search_all_url(query)
    result = await make_request(url)
    # result = result["results"]
    return result


# this func returns a list of all songs if found
@app.get("/search/song/{song_name}")
async def search_song(song_name, request: Request) -> []:
    url = song_search(song_name)
    result = await make_request(url)
    result = result["results"]
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="no song found")
    return song_search_helper(result, base_url(request))


@app.get("/song/{song_id}")
async def get_song_from_id(song_id, request: Request, use_mins: bool = False) -> Song:
    url = song_links(song_id)
    result = await make_request(url)
    if "songs" in result:
        result = result["songs"][0]
        return song_model_helper(result, use_mins, base_url(request))
    else:
        raise HTTPException(status_code=404, detail="no song found with the given id")


@app.get("/search/album/{album_name}")
async def search_album(album_name, request: Request):
    url = ablum_url(album_name)
    result = await make_request(url)
    return albumSearchHelper(result, base_url=base_url(request))


@app.get("/album/{album_id}")
async def get_album_from_id(album_id: int):
    url = album_by_id(album_id)
    result = await make_request(url)
    return result


# if the given song_id has no lyrics or even it does not exist it will give same error
@app.get("/lyrics/{song_id}")
async def get_lyrics_from_song_id(song_id) -> dict:
    url = lyrics_url(song_id)
    result = await make_request(url)
    if not "lyrics" in result:
        raise HTTPException(status_code=404, detail="lyrics not found")
    return {"lyrics": result["lyrics"]}


@app.get("/homepage-data")
async def homepage_data():
    url = get_homepage()
    result = await make_request(url)
    return result


@app.get("/create_radio/{song_id}")
async def create_radio(song_id):
    # ! : even if the song_id is wrong it will return you a station id which will give you zero songs
    url = create_radio_station(song_id)
    result = await make_request(url)
    return result


@app.get("/get_radio_songs/{station_id}")
async def get_radio_songs(
    station_id,
    request: Request,
    use_mins: bool = False,
    num_of_songs: int = 5,
    # action="fwd" or "bck",
) -> []:
    # ? : if the station id is correct you will get the songs else you will get nothing
    url = get_songs_from_radio(station_id, num_of_songs)
    result = await make_request(url)
    if "error" in result:
        raise HTTPException(
            status_code=404,
            detail="wrong station id or generated from non-existing song id",
        )
    else:
        # * : if everything goes right set the stage for result
        return radio_song_helper(result, base_url(request), use_mins)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080)
