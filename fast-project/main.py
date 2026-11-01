from fastapi import FastAPI
# from enum import Enum
from  pydantic import BaseModel

##REQUEST BOdy data sent by the client to the API : A response body is the data your API sends to the client.

# the data model
class Item(BaseModel):
  name:str
  description:str |None =None
  price: float
  tax: float |None = None


app = FastAPI()

@app.post("/items/")
async def create_item(item:Item):
  return item

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