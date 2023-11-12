from pydantic import BaseModel


# this is the std Album search response obj
class SearchEntityAlbum(BaseModel):
    id: int
    title: str
    imgs: dict
    music: str
    description: str
    song_count: int
    more_info: dict
    perma_url: str
    api_url: dict
