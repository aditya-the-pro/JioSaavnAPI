from pydantic import BaseModel


# this is the std Song response obj
from models.song import Song

# ? album obj for response
class Album(BaseModel):
    title: str
    name: str
    year: int
    release_date: str
    primary_artists:str
    primary_artists_id:int|str
    albumid: int
    perma_url:str
    imgs:dict
    songs: list[Song]
