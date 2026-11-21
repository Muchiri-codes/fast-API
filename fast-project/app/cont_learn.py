from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

router = APIRouter()

#STREAMING JSON - send one at a time
class Item(BaseModel):
  name: str
  description: str | None
  
items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@router.get("/items/stream")
#could use Iterable if the function isnt async - still okay
async def stream_items() -> AsyncIterable[Item]: # could also have no return type and it will still work well
  for item in items:
    yield item

