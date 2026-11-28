from fastapi import FastAPI
from app.database.connection import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.routers.users import router as users_router

Base.metadata.create_all(bind = engine) # create the tables
app = FastAPI()
origins ="http://localhost:3000"

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)
app.include_router(users_router)

@app.get("/api/v1/health")
def check_health():
  return {"status":"Backend is running"}

@app.get("/")
def read_root():
  return {"message":"Lets start here!"}

def main():
  return {"message":"backend initiated"}

if __name__ == "__main__":
  main()