from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def fetch_users():
  return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags =["users"])
async def read_users_me():
  return {"username":"john Muchiri"}


@router.get("/users/{username}", tags=["list"])
async def read_users(username:str):
  return {"username": username}