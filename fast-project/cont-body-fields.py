from fastapi import FastAPI, Body, Cookie, Header, Response
from typing import Annotated, Any
from pydantic import BaseModel, Field, EmailStr
from fastapi.responses import RedirectResponse

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


#RETURN TYPE - Response model
class Item(BaseModel):
  name: str
  description: str | None = None
  price : float
  tax: float | None= None
  tags: list[str] = []
  
  
@app.post("/item/", response_model=Item)
async def add_items(item: Item) -> Any:
  return item

@app.get("/item", response_model=list[Item])
async def read_items() -> Any:
  return[
    Item(name="water gun", price=456.78),
    Item(name="Plumbus",price = 556.78)
  ]
  
class BaseUser(BaseModel):
  username:str
  email: EmailStr
  full_name: str | None = None
  
  
class UserIn(BaseModel):
  #user only input the password, all other fields will be validated from the server database
  password: str
  
@app.post("/user/")
async def login(user: UserIn) -> BaseUser:
  return user

#setting the response_model to none makes fastapi to skip response model generation
@app.get("/teleport", response_model=None)
async def get_port(portal: bool= False) -> Response | dict:
  if portal:
   return RedirectResponse(url="https://johnmuchiri.vercel.app")
  return {"message":"Here is my portal"}

#response_model_exclude_unset = True/False - to remove defaulted values