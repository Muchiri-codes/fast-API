from fastapi import FastAPI, Query
from typing import Annotated

# from enum import Enum
from  pydantic import BaseModel

##REQUEST BOdy data sent by the client to the API : A response body is the data your API sends to the client.

# the data model
# class Item(BaseModel):
#   name:str
#   description:str |None =None
#   price: float
#   tax: float |None = None


app = FastAPI()

# @app.post("/items/{item_id}")
# async def create_item(item:Item):
#   item_dict = item.model_dump()
#   if item.tax is not None:
#     price_with_tax = item.price + item.tax
#     item_dict.update({"Price with tax":price_with_tax})
#   return item_dict

# class StudentName(str, Enum):
#   john="John Muchiri",
#   Leah = "Leah Muthoni",
#   juju = "Juddy Wanjiru"
  
# @app.get("/student/{student_name}")
# async def get_student(student_name:StudentName):
#   if student_name is StudentName.john:
#     return {"student_name":{student_name} , "course":"Nursing", "message":"You can go and treat the patients"}
#   if student_name.value == "Leah":
#     return {"student_name":{student_name}, "course":"Bsc Gegis", "message":"You can not do anythig in the field"}
#   return{"student_name":{student_name}, "course":"Bsc Mechatronics", "message":"You can proceed"}
    
  
# @app.get("/")
# async def root():
#   return {"message":"Hey! I am John"}


# #path ops are 
# @app.get("/items/{item_id}")
# async def read_item(item_id:int):
#   return{"item_id":item_id}



# #QUERY PARAMETERS eg. http://127.0.0.1:8000/stuff?skip=0&limit=10

# fake_items =[{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# @app.get("/stuff")
# async def get_stuff(skip: int = 0, limit:int=2):
#   return fake_items[skip : skip + limit]


# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(user_id:int, item_id:str, q:str | None = None, short:bool = False):
#   item = {"item_id":item_id, "owner_id":user_id}
#   if q:
#     item.update({"q":q})
    
#   if not short:
#     item.update(
#       {"description": "This is an amazing item that has a long description"}
#     )
#   return item

# #default values that are non-path parameters , set the default as none

# @app.get("/mothers/{mother_id}")
# async def get_mothers(mothers_name:str, health:str, tel:float | None = None):
#   mother = {"mother_name":mothers_name, "Health Status":health, "Phone number": tel}
  
#   return mother

@app.get("/items/")
async def read_items(q:Annotated[str | None, Query(min_length = 3, max_length= 50, pattern="^fixedquery$")] = None):
  result = {"items":[{"item_id":"Foo"}, {"item_id":"Bar"}]}
  if q:
    result.update({"q":q})
    
  return result

#using default values other than None

@app.get("/goods/")

async def get_goods(good:Annotated[str, Query(min_length=3, max_length=50, pattern="^good$")] = "fixedquery"):
  results = {"goods":[{"good:id":"buckets"}, {"good_id":"dishes"}]}
  if good:
    results.update({"good":good})
  return results

#declaring query parameter as a list/multiple items
@app.get("/things/")
async def get_things(q:Annotated[list[str] | None, Query()] = None):
  #must use query,else it'll be interpreted as a request boduy
  query_things = {"q":q}
  return query_things

#Query parameter list with defaults
@app.get("/animals/")
async def get_animals(q:Annotated[list[str] | None, Query(
  title = "Query string",
  description="Query items could take multiple items/list and also include defaults ",
  min_length=3,
  max_length=50,
  alias="animal-query",
  deprecated=True,
  #"include_in_schema=False" - excludes query params from te openapi schema hence in the docs
  )] = ["dogs", "fox"]):
  animal = {"q":q}
  return animal


#CUSTOM VALIDATION
from pydantic import AfterValidator
import random


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_valid_id(id:str):
  if not id.startswith(("isbn-", "-imdb-")):
    raise ValueError("Invalid ID format")
  return id

@app.get("/identity/")
async def read_id(id:Annotated[str | None, AfterValidator(check_valid_id)]= None):
  if id:
    item = data.get(id)
  else:
    id, item = random.choice(list(data.items()))
  return {"id":id, "name": item}