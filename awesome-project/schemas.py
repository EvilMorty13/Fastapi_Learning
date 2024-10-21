from datetime import date
from enum import Enum
from pydantic import BaseModel,field_validator

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'

class GenreChoices(Enum):
    ROCK = 'Rock'
    POP = 'Pop'


class Album(BaseModel):
    title : str
    release_date : date

class BandBase(BaseModel):
    name : str
    genre : GenreChoices
    albums: list[Album] = []



class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        if isinstance(value, str):
            return value.title() 
        raise ValueError('Genre must be a string')

class BandWithID(BandBase):
    id : int