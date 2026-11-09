from fastapi import FastAPI, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
  name:str
  description: str | None = Field(
    default= None, title = "Item description", max_length=300
  )
  price:float = Field(
    gt=0, description="Price must be greater than zero"
    )
  tax: float | None = None
  
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
  results = {"item_id": item_id, "item": item}
  return results