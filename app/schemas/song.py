from pydantic import BaseModel, ConfigDict, Field


class SongCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    artist: str = Field(min_length=1, max_length=200)
    album: str | None = Field(default=None, max_length=200)
    duration_seconds: int = Field(gt=0)


class SongRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    artist: str
    album: str | None
    duration_seconds: int
