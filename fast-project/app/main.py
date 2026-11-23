#global dependencies could also be declared

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Annotated
from .dependencies import get_token_header, get_query_token
from .internal import admin
from .routers import items, users, cont_learn
from fastapi.testclient import TestClient

description="""
Jonte App helps you get rich overnight

## Items
You can **read items**

## Users

You will be able to:
* **Create users** (__not implemented__).
* **Read Users** (__not implemented__)

"""

#order of metadata defines their appearance in the UI, users will go first despite being lower than items in the alphabetical order
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

fake_secret_token = "coneofsilence"
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


class Stuff(BaseModel):
    id: str
    title: str
    description: str | None = None



app = FastAPI(
  # dependencies=[Depends(get_query_token)],
  # title="Jonte's App",
  # openapi_tags=tags_metadata,
  # description=description,
  # summary="Jonte's app will make you rich overnight! ",
  # version="0.0.1",
  # terms_of_service="https://johnmuchiri/terms/",
  # contact={
  #   "name":"Muchiri john the great",
  #   "url":"https://x-force.example.com/contact",
  #   "email":"muchiri@gmail.com",
  # },
  # license_info={
  #   "name":"Jonte 3.6",
  #   "url":"https://johnmuchiri.vercel.app",
  #   "identifier":"Jonte-3.6"
  # }
  
  )


app.include_router(users.router)
app.include_router(items.router)
app.include_router(cont_learn.router)
app.include_router(
  admin.router,
  prefix="/admin",
  tags=["admin"],
  dependencies=[Depends(get_token_header)],
  responses={418:{"description":"I am a teapot"}}
)


 
@app.get("/stuffs/{stuff_id}", response_model=Stuff)
async def read_main(stuff_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if stuff_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[stuff_id]
  
@app.post("/stuffs/")
async def create_item(stuff: Stuff, x_token: Annotated[str, Header()]) -> Stuff:
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if stuff.id in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists")
    fake_db[stuff.id] = stuff.model_dump()
    return stuff
  



