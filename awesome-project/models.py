from datetime import date
from enum import Enum
from pydantic import BaseModel,field_validator
from sqlmodel import SQLModel,Field,Relationship

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'

class GenreChoices(Enum):
    ROCK = 'Rock'
    POP = 'Pop'


class AlbumBase(SQLModel):
    title : str
    release_date : date
    band_id :int | None = Field(foreign_key="band.id")

class Album(AlbumBase,table=True):
    id : int = Field(default=None,primary_key=True)
    band : "Band" = Relationship(back_populates="albums")

class BandBase(SQLModel):
    name : str
    genre : GenreChoices




class BandCreate(BandBase):
    albums: list[AlbumBase] | None=None

    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        if isinstance(value, str):
            return value.title() 
        raise ValueError('Genre must be a string')

class Band(BandBase,table=True):
    id:int = Field(default=None,primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")



