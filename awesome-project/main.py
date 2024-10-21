from fastapi import FastAPI,HTTPException, Path,Query
from schemas import GenreURLChoices,BandBase,BandCreate,BandWithID
from typing import Annotated
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
async def bands(genre:GenreURLChoices | None=None,q: Annotated[str | None,Query(max_length=10)]=None) -> list[BandWithID]:
    band_list = [BandWithID(**b) for b in BANDS]

    if genre:
        band_list = [
           b for b in band_list if b.genre.value.lower() == genre.value
        ]
    
    if q:
        band_list = [
            b for b in band_list if q.lower() in b.name.lower()
        ]

    return band_list


@app.get('/bands/{band_id}')
async def band(band_id:Annotated[int,Path(title="The band ID")]) -> BandWithID :
    band = next((BandWithID(**b) for b in BANDS if b['id']==band_id),None)
    if band is None:
        raise HTTPException(status_code=404,detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre:GenreURLChoices) -> list[dict] :
    return[
        b for b in BANDS if b['genre'].lower() == genre.value
    ]



@app.post("/bands")
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1  # Corrected ID generation
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band

