from fastapi import FastAPI, Depends, Query
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Annotated
from contextlib import asynccontextmanager

class Hero(SQLModel, table = True):
  id: int |None = Field(default=None, primary_key= True)
  name: str
  secret_name: str
  age: int | None = Field(default=None, index= True)
  
#create the engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

#create the tables
def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

#session stores the objects in memory
def get_session():
  with Session(engine) as session: #open a session
    yield session
    
sessionDep = Annotated[Session, Depends(get_session)]
    
     
@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield
  
app = FastAPI(lifespan=lifespan)

@app.post("/heroes/") # create a row
def create_hero(hero: Hero, session: sessionDep) -> Hero:
  session.add(hero) #stage it
  session.commit() #save to db
  session.refresh(hero) # reload from db
  return hero # respond


#read the heroes
@app.get("/heroes/")
def read_heroes(
  session: sessionDep,
  offset:int=0,
  limit: Annotated[int, Query(le=100)] = 100,  #prevent requesting too many rows 
  
) -> list[Hero]:
  heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
  return heroes