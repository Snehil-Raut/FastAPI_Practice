# simple initial start

from fastapi import FastAPI
from fastapi.params import Body

from . import schemas
from typing import Optional
app = FastAPI()

# request Get method url: "/" -- finds a match

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_post():
    return {"message": "list multiple posts"}

@app.post("/createposts")
def create_posts(new_Post: schemas.Post):
    print(new_Post.title) # access each property only the value
    print(new_Post.content)
    print(new_Post.published)
    print(new_Post.rating)      # default to none if nothing mentioned
    print(new_Post.model_dump())  # convert the data to dict which comes from postman
    return {"data": new_Post}