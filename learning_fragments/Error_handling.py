#errors could be: no access to ssome resource, no privileges for an operation or that the requested item does not exist  etc
#Code ranges would be 400 to 499

# 1. HTTPException
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteException
from pydantic import BaseModel
from enum import Enum




app = FastAPI()



#student will be the id
items = {"student":"john_muchiri"}

@app.get("/items/{item_id}")
async def read_items(item_id: str):
  if item_id not in items:
    raise HTTPException(
      status_code=404, 
      detail="Item not Found",
      headers={"X-error": "There goes my error"} # rarely used
      )
    
  return {"item": items[item_id]}

class UnicornException(Exception):
  def __init__(self, name: str):
    self.name = name
    

#Installing custom exceptions
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
  return JSONResponse(
    status_code= 418,
    content={"message": f"Ooops! {exc.name} did something, there goes a rainbow..."}
  )
  
@app.get("/unicorns/{name}")
async def raed_unicorn(name: str):
  if name == "yolo":
    raise UnicornException(name = name)
  return {"unicorn_name": name}
  
#OVERIDING FASTAPI DEFAULT EXCETION HANDLERS with my own
@app.exception_handler(StarletteException)
async def http_exception_handler(request ,exc):
  return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
  

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
  message = "Validation Errors:"
  for error in exc.errors():
    message += f"\nField: {error['loc']}, error: {error['msg']}"
  return PlainTextResponse(message, status_code=400)

@app.get("/item/{item_id}")
async def read_items(item_id: int):
  if item_id == 3:
    raise HTTPException(status_code= 418, detail = " 3 IS PROHIBITED!!")
  return {"item_id": item_id}

#PATH OPERATION CONFIGURATIO
class Goods(BaseModel):
  name: str
  descripton: str | None = None
  price: float
  tax: float | None = None
  tags: set[str] = set()

#passing status code
@app.post("/goods", status_code=status.HTTP_201_CREATED)
async def get_goods(good: Goods) -> Goods:
  return good

#adding tags - usually a list of one str - helps classify
# @app.get("/goods", tags=["goods"])
# async def read_goods():
#   return [{"name": "goat", "price": 450}]

# @app.get("/users/", tags=["users"] )
# async def read_users():
#   return [{"username": "johndoe"}]


#enum creates a collection of value/pair 
class Tags(Enum):
  item = "items"
  users="users"
  
@app.get("/things/", tags = [Tags.item])
async def read_things():
  return ["portal fun","laser gun"]

@app.get("/people/", tags=[Tags.users])
async def read_people():
  return ["John", "Muchiri", "wanjiru"]

#adding summary and descripton in the decorator call
@app.post(
  "/goods/",
  summary="creates a good",
  # description="creates an item with all iinfo such as name, description, price, tax and tags"
  response_description="the created good",
  deprecated=True #mark path operation as deprecated without removing it 
  )
async def create_good(good: Goods) -> Goods:
  #description from docstring
  """
  Create an item with all the information:
  - **name**: each item must have a name
  - **description** : A long description
  - **price** : Required
  - **tax**: if the item desnt have tax, you can omit this
  - **tags**: a set of unique tag strings for this item 
  """
  
  return good

#converting a data type to one compatible with json like a dict/list
from fastapi.encoders import jsonable_encoder
from datetime import datetime

fake_db  ={}

class Tools(BaseModel):
  title: str
  timestamp: datetime
  description: str | None = None
  
@app.put("/items/{id}")
def update_item(id: str, item: Tools) -> Tools:
  json_compatible_data= jsonable_encoder(item) #will convert item data to json data - Pydantic model to a dict, and the datetime to a str
  fake_db[id]=json_compatible_data
  
