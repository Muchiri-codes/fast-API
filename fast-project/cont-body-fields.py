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


#COOKIE PARAMS MODEL
class Preference(BaseModel):
  theme: str
  locale: str
  
class CommonHeaders(BaseModel):
  model_config={'extra': "forbid"}
  host: str
  save_data: bool
  if_modified_since: str | None = None
  traceparent: str |None = None
  X_tag : list[str] =[]
  
@app.get("/preference/")
async def get_preferences(
  preferences: Annotated[Preference | None, Cookie()] = None, headers: Annotated[CommonHeaders, Header(convert_underscores=False)] = None):
  return {"preference_cookies": preferences, "headers": headers}



#HEADER PARAMS MODELS
