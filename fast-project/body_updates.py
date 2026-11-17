from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
  name: str | None = None
  description: str | None = None
  price: float | None = None
  tax: float = 10.5
  tags:list[str] = []

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
  return items[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item) -> Item:
  stored_item_data = items[item_id] #grab raw dict {"name": "Foo", "price": 50.2}
  stored_item_model = Item(**stored_item_data) #Builds a full Item model — Pydantic fills in defaults: description=None, tax=10.5, tags=[]
  update_data = item.model_dump(exclude_unset=True)# Converts the request body to a dict, but only keeps fields the client explicitly sent.
  updated_item = stored_item_model.model_copy(update=update_data) #creating a copy of existing model using .model_copy() and ovewrites only the keys in update_data
  items[item_id] = jsonable_encoder(updated_item)
  return updated_item


#partial updates with patch - rarely used, put is usually used


