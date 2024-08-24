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


my_posts = [{"id": 1, "title": "Post 1", "content": "This is post 1"}, {"id": 2, "title": "Post 2",
                                                                        "content": "This is post 2"}, {"id": 3, "title": "Post 3", "content": "This is post 3"}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# decorator. This contains the FastAPI instance and the path to be accessed. It can either be called an API route or Path Operation.
@app.get("/")
async def root():  # function. The async keywork is optional, it is used to indicate that the function is asynchronous, i.e., communicating with the Database, etc.
    return {"status": "success", "code": 200, "error": False,  "message": "API is working!", "data": {}}


@app.get("/posts")
def get_posts():
    return {"status": "success", "code": 200, "error": False,  "message": "These are your posts", "data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    # Here we will be using Pydantic to define a schema for our payload. This will restrict the user to follow the schema and he cannot send any garbage value in the POST Body.
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"status": "success", "code": 201, "error": False,  "message": "New post created successfully", "data": my_posts}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)
    return {"status": "success", "code": 200, "error": False,  "message": "Post fetched successfully", "data": post}
