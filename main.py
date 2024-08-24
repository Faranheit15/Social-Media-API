from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
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


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

# decorator. This contains the FastAPI instance and the path to be accessed. It can either be called an API route or Path Operation.


@app.get("/")
async def root():  # function. The async keywork is optional, it is used to indicate that the function is asynchronous, i.e., communicating with the Database, etc.
    return {"status": "success", "code": status.HTTP_200_OK, "error": False,  "message": "API is working!", "data": {}}


@app.get("/posts")
def get_posts():
    return {"status": "success", "code": status.HTTP_200_OK, "error": False,  "message": "These are your posts", "data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Here we will be using Pydantic to define a schema for our payload. This will restrict the user to follow the schema and he cannot send any garbage value in the POST Body.
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"status": "success", "code": status.HTTP_201_CREATED, "error": False,  "message": "New post created successfully", "data": my_posts}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"status": "error", "code": 404, "error": True,  "message": f"Post with ID {id} not found", "data": {}}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    return {"status": "success", "code": status.HTTP_200_OK, "error": False,  "message": "Post fetched successfully", "data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    my_posts.pop(index)
    return {"status": "success", "code": status.HTTP_204_NO_CONTENT, "error": False,  "message": "Post deleted successfully", "data": my_posts}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"status": "success", "code": status.HTTP_200_OK, "error": False,  "message": "Post updated successfully", "data": my_posts}
