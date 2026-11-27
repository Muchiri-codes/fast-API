from fastapi import FastAPI
from app.models.user import User
from app.database.connection import engine

User.metadata.create_all(bind = engine) # create the tables
app = FastAPI()

@app.get("/")
def read_root():
  return {"message":"Lets start here!"}

def main():
  return {"message":"backend initiated"}

if __name__ == "__main__":
  main()