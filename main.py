import uvicorn
from fastapi import FastAPI, Request
import httpx
import endpoints
import helper

# * INFO : experimental


# TODO : add the playlist, homepage, radio features

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def make_request(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            exit({"msg": "server ip got banned for api rate limits"})
        else:
            exit({"msg": "unknown server error go debug it"})


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


@app.get("/test")
async def test_handler(request: Request):
    return {"link": base_url(request)}

# make a decorator for mchecking remote reuqets for http error 202 and 500


if __name__ == "__main__":
    # disable reloder while deploying it to vercel
    # uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True) for making changes
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
