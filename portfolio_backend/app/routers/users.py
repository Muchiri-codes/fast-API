from fastapi import APIRouter, Depends, HTTPException, status
from app.models.join_team import UserResponse, UserCreate
from app.database.connection import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User



router = APIRouter(
  prefix="/api/v1/users",
  tags=["users"]
)



@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
  user_data: UserCreate, 
  db:Session=Depends(get_db)
  ):
  existing_username=db.query(User).filter(
    User.username ==user_data.username
  ).first()
  
  if existing_username:
     raise HTTPException(
       status_code=status.HTTP_409_CONFLICT, 
       detail="User already exist"
     )
     
  existing_email= db.query(User).filter(
    User.email== user_data.email
  ).first()
  
  if existing_email:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="email already exist"
    )
    
  new_user = User(
    username = user_data.username,
    email=str(user_data.email)
  )
  
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
  except IntegrityError:
    db.rollback()
    raise HTTPException(
      status_code= status.HTTP_409_CONFLICT, 
      detail="Either username or email already exists"
    )
    
  return new_user