from fastapi import Depends, APIRouter
from database.connection import get_db
from sqlalchemy.orm import Session
from models.user import User


router = APIRouter(
  prefix='/users',
  tags=["users"]
)
def init_db():
  db = Session()
  for user in User:
    db.add(user)
  
  
  
@router.post("/")
async def add_user(username : str, email: str, db:Session=Depends(get_db)):
  user = User(
    username = username,
    email =email
  )