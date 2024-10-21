from datetime import date
from enum import Enum
from pydantic import BaseModel

class GenreURLChoices(Enum):
    ROCK = 'rock'
    POP = 'pop'

class Album(BaseModel):
    title : str
    release_date : date

class Band(BaseModel):
    id : int
    name : str
    genre : str
    albums: list[Album] = []




