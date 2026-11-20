# Middlewares - fns that intercepts every request before it reaches your route handlers and can also modify every response before it's sent back to the client
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins= origins, #any allowed origin
  allow_credentials= True, # allow cookies
  allow_methods=["*"], # * for all http methods
  allow_headers=["*"]
)

@app.get("/items")
async def main():
  return {"message": "Hey guys!"}
app.middleware("http")
async def add_process_time_header(request: Request, call_next):
  start_time = time.perf_counter()
  response = await call_next(request) #pass the req to the route handler and get the response 
  process_time = time.perf_counter()- start_time
  response.headers["X-Process-Time"] = str(process_time)#modify the value of "XProcess-Time" before returing it
  return response 

#CORS - situations when a frontend has js code that communicates with backend, and the backend is in a different origin 
# * means that all are allowed