from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
app = FastAPI()

#Userbase class will be used in all the other models
class UserBase(BaseModel):
  username: str
  email: EmailStr
  fullname : str | None = None
  
  
class UserIn(UserBase):
  password: str

   
class UserOut(UserBase): # its using userbase for the other fiels, only the unique one is being retained
  pass

class UserInDb(UserBase):
  hashed_password : str

  
def hash_password(raw_password: str):
  return "supersecret" + raw_password

def save_in_DB(user_in: UserIn):
  hashed_pass= hash_password(user_in.password)
  #.model.dump() returns a dict with the models data
  user_in_db = UserInDb(**user_in.model_dump(), hashed_password= hashed_pass)
  print("user saved! Not realy bro")
  return user_in_db
  
@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
  saved_user = save_in_DB(user_in)
  return saved_user
  
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

#responses can also be a list of objects
@app.get("/items/", response_model=list[Item])
async def read_items():
    return items
  
  