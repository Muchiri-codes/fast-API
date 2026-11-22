from collections.abc import AsyncIterable, Iterable
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

router = APIRouter()

#STREAMING JSON - send one at a time
class Item(BaseModel):
  name: str
  description: str | None

class Stuff(BaseModel):
  name: str
  price: float
  
class Prompt(BaseModel):
  text: str



stuffs = [
    Stuff(name="Plumbus", price=32.99),
    Stuff(name="Portal Gun", price=999.99),
    Stuff(name="Meeseeks Box", price=49.99),
]
items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@router.get("/things/stream")
#could use Iterable if the function isnt async - still okay
async def stream_items() -> AsyncIterable[Item]: # could also have no return type and it will still work well
  for item in items:
    yield item


#STREAMING DATA VIA SSE
#this streams data from server to client over a http
#SSE is mostly used for AI chat streaming, live notifications, logs and other cases where the server pushes updates to the client
#EventSourceResponse is used as the class
#Return could be async, normal or even  no return type and it will work
@router.get("/goods/stream", response_class=EventSourceResponse)
async def sse_items() -> AsyncIterable[Item]:
   for item in items:
     yield item

@router.get("/stuff/stream", response_class=EventSourceResponse)
async def stream_stuff() -> AsyncIterable[ServerSentEvent]:
  yield ServerSentEvent(comment="stream of stuff updates")# keeps the connection alive, executed first - then evvey 15s
  for i, stuff in enumerate(stuffs): #iterate through stuffs list
    yield ServerSentEvent(data = stuff, event="stuff_update", id=str(i + 1),retry=5000)
    
@router.post("/chat/stream", response_class= EventSourceResponse)
async def stream_chat(prompt: Prompt) -> AsyncIterable[ServerSentEvent]:
  words = prompt.text.split()
  for word in words:
    yield ServerSentEvent(data = word, event="token")
  yield ServerSentEvent(raw_data='[DONE]', event="done")
  
  
#BACKGROUND TASKS

def write_log(message:str):
  with open("log.txt", mode="a") as log:
    log.write(message)

def get_query(background_tasks:BackgroundTasks, q:str| None = None):
  if q:
    message =f"found query: {q}\n"
    background_tasks.add_task(write_log, message)
  return q 

@router.post("/notifications/{email}", tags=["notifications"])
async def send_notification(
  email:str,
  background_tasks:BackgroundTasks, 
  q:Annotated[str, Depends(get_query)] #call get_query and use its return value
):
  message=f"message to {email}\n"
  background_tasks.add_task(write_log, message)
  return {"message":"Message sent"}