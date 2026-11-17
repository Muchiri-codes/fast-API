#NB . Securiy is a complex topic - could take 50% of the written code

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Oauth2PasswordBearer -uses OAuth2, with the Password flow, using a Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # receieves the username and password from the frontend
# token url is the url the client will use to send the username and password inorde to get the client

@app.get("/items/")
async def read_items(token:Annotated[str, Depends(oauth2_scheme)]):
  return {"token": token}