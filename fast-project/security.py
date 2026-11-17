#NB . Securiy is a complex topic - could take 50% of the written code

from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# Oauth2PasswordBearer -uses OAuth2, with the Password flow, using a Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # url receieves the username and password from the frontend
# token url is the url the client will use to send the username and password inorde to get the client

class User(BaseModel):
  username: str
  email: str | None = None
  full_name: str | None = None
  disabled: bool | None = None
  
def fake_decode_token(token):
  return User(
    username = token + "fakecoded", email="john@gmail.com", full_name="John Muchiri"
  )
  
async def get_current_uer(token: Annotated[str, Depends(oauth2_scheme)]):
  user = fake_decode_token(token)
  return user


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_uer)]):
  return current_user