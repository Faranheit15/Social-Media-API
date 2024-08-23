from fastapi import FastAPI
from fastapi.params import Body  # accessing POST body
from pydantic import BaseModel  # schema
from typing import Optional

app = FastAPI()  # initializing the FastAPI instance


class Post(BaseModel):  # define the schema for our POST Body
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# decorator. This contains the FastAPI instance and the path to be accessed. It can either be called an API route or Path Operation.


@app.get("/")
async def root():  # function. The async keywork is optional, it is used to indicate that the function is asynchronous, i.e., communicating with the Database, etc.
    return {"status": "success", "code": 200, "error": False,  "message": "API is working!", "data": {}}


@app.get("/posts")
def get_posts():
    return {"status": "success", "code": 200, "error": False,  "message": "These are your posts", "data": [{"title": "Post 1", "content": "This is post 1"}, {"title": "Post 2", "content": "This is post 2"}, {"title": "Post 3", "content": "This is post 3"}]}


@app.post("/create_post")
def create_post(new_post: Post):
    # Here we will be using Pydantic to define a schema for our payload. This will restrict the user to follow the schema and he cannot send any garbage value in the POST Body.
    print(new_post.dict())
    return {"status": "success", "code": 200, "error": False,  "message": "New post created successfully", "data": new_post}
