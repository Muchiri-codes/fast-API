# DEPENDENCY INJECTION
#A way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies". - minimize code repetition
from fastapi import FastAPI, Depends, Cookie, Header, HTTPException
from typing import Annotated

app = FastAPI()

async def common_params(q: str  |  None = None, skip: int=0, limit:int=100):
  return {"q": q, "skip":skip, "limit": limit}

#Depends only takes one param and that is a function-like param eg common_params

# assign it a variable to avoid duplication - type alias
commonDeps = Annotated[dict, Depends(common_params)]

@app.get("/items")
async def read_items(commons: commonDeps):
  return commons


@app.get("/users")
async def read_users(commons: commonDeps):
  return commons
    
    
#CLASSES AS DEPENDENCIES
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
  def __init__(self, q: str | None = None, skip: int =0, limit:int =100):
    self.q = q
    self.skip = skip
    self.limit = limit
    
@app.get("/item")
#the first CommonQueryParas is used or data validation, no meaning to FastApi, could be set to "any"
#the second is what is used to inject the dependencies
async def read_item(commons: Annotated[CommonQueryParams, Depends()]):
    response ={} # initiate the response variable as an empty dict
    if commons.q:
      response.update({"q":commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
  
  
  
  #SUBDEPENDENCIES
  #1st dependency
def query_extractor(q: str | None = None):
  return q
# 2nd dependable/dependant
def query_cookie_extractor(
  q: Annotated[str, Depends(query_extractor)],
  last_query: Annotated[str | None, Cookie()] = None
):
  if not q:
    return last_query
  return q

#we now use the dependency
@app.get("/cows")
async def read_query(
  query_or_default: Annotated[str, Depends(query_cookie_extractor)],
):
  return {
    "q_or_cookie": query_or_default
  }
  
# Dependencies that dont return a value or the return value isnt needed but still want to execute the dependency
#For those cases, instead of declaring a path operation function parameter with Depends, you can add a list of dependencies to the path operation decorator.
def x_token_verify(x_token: Annotated[str, Header()]):
  if x_token !="super_x_value":
    raise HTTPException(status_code=400, detail ='Wrong value for the x_token')

async def x_key_verify(x_key: Annotated[str,Header()]):
  if x_key != "some-super-key":
    raise HTTPException(status_code = 400, detail="Wrong x_key")
  return x_key


# to define global dependencies in fastApi
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
@app.get("/verify/", dependencies=[Depends(x_token_verify), Depends(x_key_verify)])
async def verify_token_key():
  return [{"item":"foo"}, {"item":"bull"}]
  
  
#DEPENDENCIES WITH YIELD
# if the dependeny can do extra steps after finishing, use yield instead of return

#yield turns the dependency into a two-part function: the first half runs before your route, the second half runs after — and FastAPI is the thing that "unpauses" it

def get_db():
  print("A: Opening session")
  db = sessionLoacal()
  try:
    print ("B: Handing DB to Route")
    yield db
  finally:
    print("C: closing session")
    db.close()