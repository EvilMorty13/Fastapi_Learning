from fastapi import FastAPI,HTTPException
from schemas import GenreURLChoices,Band

app = FastAPI()


BANDS = [
    {"id":1,'name':'The Beatles','genre':'Rock'},
    {"id":2,'name':'One Direction','genre':'Pop'},
    {"id":3,'name':'Linkin Park','genre':'Rock','albums':[
        {'title':'Hybrid Theory','release_date':'2000-10-24'}
    ]},
    {"id":4,'name':'Backsteet Boys','genre':'Pop'},
]


@app.get('/bands')
async def bands(genre:GenreURLChoices | None=None,has_albums:bool=False) -> list[Band]:
    band_list = [Band(**b) for b in BANDS]
    if genre:
        band_list = [
           b for b in band_list if b.genre.lower() == genre.value
        ]

    if has_albums: 
        band_list = [b for b in band_list if len(b.albums)>0]

    return band_list


@app.get('/bands/{band_id}')
async def band(band_id:int) -> Band :
    band = next((Band(**b) for b in BANDS if b['id']==band_id),None)
    if band is None:
        raise HTTPException(status_code=404,detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre:GenreURLChoices) -> list[dict] :
    return[
        b for b in BANDS if b['genre'].lower() == genre.value
    ]