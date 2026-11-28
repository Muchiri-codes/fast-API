from pydantic import BaseModel, ConfigDict, EmailStr, Field

#front must send
class UserCreate(BaseModel):
  username : str = Field(min_length=3, max_length=100)
  email: EmailStr
  
  #backend will return
class UserResponse(BaseModel):
  id: int
  username: str
  email: EmailStr
  
  model_config=ConfigDict(from_attributes=True)
  