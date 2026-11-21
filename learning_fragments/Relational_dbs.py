from fastapi import FastAPI, Depends, Query, APIRouter
from sqlmodel import Field, SQLModel, create_engine, Session, select
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi.exceptions import HTTPException

 #data model 
class HeroBase(SQLModel):
  name: str = Field(index=True) # easier for SELECT * WHERE name ="student"
  age: int | None = Field(default=None, index = True)
  
#table model
class Hero(HeroBase, table = True):
  id: int |None = Field(default=None, primary_key= True)
  secret_name: str
  
class HeroPublic(HeroBase): #SENT to the client
  id: int
  
class HeroCreate(HeroBase): #validates users input
  secret_name: str
  
class HeroUpdate(HeroBase): #all fields are optional so you can update any
  name: str | None = None
  age:int | None = None
  secret_name: str | None = None
  
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
    
SessionDep = Annotated[Session, Depends(get_session)]
    

#table creation runs once on page load  
@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield
  
app = FastAPI(lifespan=lifespan)

@app.post("/heroes/", response_model=HeroPublic) # create a row
def create_hero(hero: HeroCreate, session: SessionDep):
  db_hero = Hero.model_validate(hero) #convert schema to table
  session.add(db_hero) #stage it
  session.commit() #save to db
  session.refresh(db_hero) # reload from db
  return db_hero # respond


#read the heroes
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
  session: SessionDep,
  offset:int=0,
  limit: Annotated[int, Query(le=100)] = 100,  #prevent requesting too many rows 
  
):
  heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
  return heroes

#read one hero with HeroPublic
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
  hero = session.get(Hero, hero_id) # fethc a row of type Hero model whose primary key is "hero_id"
  if not hero:
    raise HTTPException(status_code=404, detail="Hero Not Found!")
  return hero

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int,hero:HeroUpdate, session:SessionDep):
  herodb = session.get(Hero, hero_id)
  if not herodb:
    raise HTTPException(status_code=404, detail="Hero Not Found")
  hero_data = hero.model_dump(exclude_unset=True)
  #model.dump() -covert the model into a plain dict
  #exlude_unset - omit any field the client didnt send regardless of its default
  herodb.sqlmodel_update(hero_data) # apply the changes 
  session.add(herodb)
  session.commit()
  session.refresh(herodb)
  return herodb



@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int ,session:SessionDep):
  hero = session.get(Hero, hero_id)
  if not hero:
    raise HTTPException(
      status_code = 404, detail="Hero not found"
    )
  session.delete(hero)
  session.commit()
  return {"ok": True}

router = APIRouter()

@router.get("/users/", tags = ["users"])
async def read_users():
  return [{"Username":"Rick"}, {"Username": "Jonte"}]