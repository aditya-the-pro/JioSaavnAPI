import uvicorn
from fastapi import FastAPI, Request, HTTPException
import httpx
import endpoints
import helper

# * INFO : experimental


# TODO : add the playlist, homepage features and more :)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def make_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            raise HTTPException(
                status_code=200,
                detail={"msg": "server ip got banned for api rate limits"},
            )
        else:
            raise HTTPException(
                status_code=200, detail={"msg": "unknown server error go debug it"}
            )


def base_url(request: Request):
    return request.base_url._url


@app.get("/")
async def root():
    return {"msg": "Yes, its working fine !"}


@app.get("/search/song/{name}")
async def search_handler(name):
    url = endpoints.song_search(name)
    result = await make_request(url)
    result = result["results"]
    return helper.resultRender(result)


@app.get("/song/{song_id}")
async def song_handler(song_id):
    url = endpoints.song_links(song_id)
    result = await make_request(url)
    if "songs" in result:
        result = result["songs"][0]
        return helper.jsonDataMaker(result)
    else:
        return {"msg": "invalid song id"}


@app.get("/search/album/{album_name}")
async def album_search(album_name, request: Request):
    url = endpoints.ablum_url(album_name)
    result = await make_request(url)
    return helper.albumSearchHelper(result, base_url=base_url(request))


@app.get("/album/{album_id}")
async def album_handler(album_id: int):
    url = endpoints.album_by_id(album_id)
    result = await make_request(url)
    return result


@app.get("/lyrics/{song_id}")
async def lyrics_handler(song_id):
    url = endpoints.lyrics_url(song_id)
    result = await make_request(url)
    return helper.lyricsHelper(result)


@app.get("/homepage-data")
async def homepage_data():
    url = endpoints.get_homepage()
    result = await make_request(url)
    return result


@app.get('/create_radio/{song_id}')
async def create_radio(song_id):
    # ! : even if the song_id is wrong it will return you a station id which will give you zero songs
    url = endpoints.create_radio_station(song_id)
    result = await make_request(url)
    return result


@app.get('/get_radio_songs/{station_id}')
async def get_radio_songs(station_id):
    # ? : if the station id is correct you will get the songs else you will get nothing
    url = endpoints.get_songs_from_radio(station_id)
    result = await make_request(url)
    if "error" in result:
        raise HTTPException(
            status_code=404,
                detail={"msg": "wrong station id or generated from non-existing song id"},
        )
    else :
        # * : if everything goes right set the stage for result
        return helper.radio_song_helper(result)


if __name__ == "__main__":
    # disable reloder while deploying it to vercel
    # uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
