#global dependencies could also be declared

from fastapi import Depends, FastAPI
from .dependencies import get_token_header, get_query_token
from .internal import admin
from .routers import items, users, cont_learn

description="""
Jonte App helps you get rich overnight

## Items
You can **read items**

## Users

You will be able to:
* **Create users** (__not implemented__).
* **Read Users** (__not implemented__)

"""

#order of metadata defines their appearance in the UI, users will go first despite being lower than items in the alphabetical order
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
  dependencies=[Depends(get_query_token)],
  title="Jonte's App",
  openapi_tags=tags_metadata,
  description=description,
  summary="Jonte's app will make you rich overnight! ",
  version="0.0.1",
  terms_of_service="https://johnmuchiri/terms/",
  contact={
    "name":"Muchiri john the great",
    "url":"https://x-force.example.com/contact",
    "email":"muchiri@gmail.com",
  },
  license_info={
    "name":"Jonte 3.6",
    "url":"https://johnmuchiri.vercel.app",
    "identifier":"Jonte-3.6"
  }
  
  )


app.include_router(users.router)
app.include_router(items.router)
app.include_router(cont_learn.router)
app.include_router(
  admin.router,
  prefix="/admin",
  tags=["admin"],
  dependencies=[Depends(get_token_header)],
  responses={418:{"description":"I am a teapot"}}
)

@app.get("/")
async def root():
  return {"message":"Hello bigger apps"}



