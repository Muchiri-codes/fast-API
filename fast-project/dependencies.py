# DEPENDENCY INJECTION
#A way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies". - minimize code repetition
from fastapi import FastAPI, Depends
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
    