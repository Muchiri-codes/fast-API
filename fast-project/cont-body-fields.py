from fastapi import FastAPI, Body, Cookie, Header
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

#COOKIE PARAMETRS
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()]= None):
  return {"ads_id": ads_id}



#HEADER PARAMS - Defined the same way as cookie, query and path

@app.get("/goats/")
#declaring duplicate headers - same header but multiple values, use list
async def get_items(x_token:Annotated[list[str] | None, Header()]=None):
  return {"X-token values": x_token}