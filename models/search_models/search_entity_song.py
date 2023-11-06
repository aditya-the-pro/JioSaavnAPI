from pydantic import BaseModel,Field


class SearchEntitySong(BaseModel):
    id: str = Field(max_length=8)
    title: str
    imgs: dict
    album: str
    description: str
    more_info: dict
    perma_url: str
    api_url: dict
