from pydantic import BaseModel, Field


# ? song obj for response
class Song(BaseModel):
    id: str = Field(max_length=8, min_length=8)
    song: str
    album: str
    year: int
    primary_artists: str
    singers: str
    imgs: dict
    duration: str | int  # it may be in secs or mins:secs
    # TODO : for duration have a query param for user to select what they want
    label: str
    album_id: int
    language: str
    copyright_text: str
    has_lyrics: bool
    links: dict
    perma_url: str
    album_url: str
    release_date: str
    api_url: dict
