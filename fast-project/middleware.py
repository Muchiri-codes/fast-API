# Middlewares - fns that intercepts every request before it reaches your route handlers and can also modify every response before it's sent back to the client
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  start_time = time.perf_counter()
  response = await call_next(request) #pass the req to the route handler and get the response 
  process_time = time.perf_counter()- start_time
  response.headers["X-Process-Time"] = str(process_time)#modify the value of "XProcess-Time" before returing it
  return response 