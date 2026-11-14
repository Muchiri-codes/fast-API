from fastapi import FastAPI, status, Form, File, UploadFile
from typing import Annotated,Literal
from pydantic import BaseModel, EmailStr
from fastapi.responses import HTMLResponse

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
@app.post("/items/", response_model=list[Item], status_code = status.HTTP_201_CREATED)
async def read_items():
    return items
  
# Status codes 
# 100 - 199 - information, rarely used, they dont have a body
# 200 - 299 - success
# 200 - Ok 
# 201 - created eg. a record was created successfully in the DB
# 204 - No ConnectionResetError

# 300 - 399 - Redirection
# 304 - Not modified

# 400 - 499 Client error 
# 400 - geeneric usage for any client error

# 500 - 599 - server errors - almost never used


#RECEIVING FORM DATA
@app.post("/login")
async def login_user(username: Annotated[str, Form()] ,password:Annotated[str, Form()]):
  
  return{"username": username}


#bool with a false default makes you receive false when a checkbox was left unchecked since it is usually ommitted by browsers
@app.post("/preferences")
async def set_preferences(sunscribe: Annotated[bool, Form()] = False):
  return{"subscribe": sunscribe}


#===============FORM MODELS====================
#To use forms, first install python-multipart
#pydantic model for forms

class FormData(BaseModel):
  username: str
  password: str
  # model_config={"extra":"forbid"} - will reject any field outside this 
  
class Specific(BaseModel):
  tags:list[str]  =[]
  
@app.post("/add")
async def add_login(
  data: Annotated[FormData, Form()],
  token: Annotated[str , Form()],
  preferences:Annotated[Specific, Form()]):
  return {"data": data, "preferences": preferences, "token": token}



class Profile(BaseModel):
  name: str
  kind: Literal["person"]
  
class Company(BaseModel):
  kind: Literal["company"]
  company_name: str
  
@app.post("/profiles/")
async def create_profile(
  #discriminator decides what moldel to uild response for
  contact: Annotated[ Profile | Company | None, Form(discriminator="kind")] = None
):
  return contact

#Request files - define files to be uploaded by the client
# adding a None and initialzing it as None makes the file optional
# extra metadata can be added inside the File()
@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File(description="A file read as bytes")]= None):
  if not file:
    return{"message": "No file sent!"}
  else:
    return {"file_size": len(file)}

@app.post("/uploadfile/")
#UploadFile has advatages over bytes, no File()
async def create_upload_file(file: Annotated[UploadFile | None, File(description="A file read as an upload")]= None):
  if not file:
    return {"message":"You did not upload any file"}
  else:
    return {"filename": file.filename}
  

#Adding multiple images - ue list
@app.post("/images/")
async def add_images(files:Annotated[list[bytes], File()]):
  return {"file sizes":[len(file) for file in files]}

@app.post("/uploadimages/")
async def create_image_upload(files: list[UploadFile]):
  return {"filenames": [file.filename  for file in files]}


@app.get("/")
async def main():
  content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
  return HTMLResponse(content=content)
