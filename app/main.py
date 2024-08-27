from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel  # schema
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from sqlalchemy.orm import Session
from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)  # this line creates the table

app = FastAPI()  # initializing the FastAPI instance


class Post(BaseModel):  # define the schema for our POST Body
    title: str
    content: str
    # published: bool = True
    # rating: Optional[int] = None


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="social-media",
#                                 user="postgres", password="postgres", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successful", cursor)
#         break
#     except Exception as error:
#         print("Error while connecting to database", error)
#         sleep(2)

# decorator. This contains the FastAPI instance and the path to be accessed. It can either be called an API route or Path Operation.


@app.get("/")
async def root():  # function. The async keywork is optional, it is used to indicate that the function is asynchronous, i.e., communicating with the Database, etc.
    return {"status": "success", "status_code": status.HTTP_200_OK, "error": False,  "message": "API is working!", "data": {}}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # using SQL
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # using SQLAlchemy
    posts = db.query(models.Post).all()
    return {"status": "success", "status_code": status.HTTP_200_OK, "error": False,  "message": "These are your posts", "data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # Here we will be using Pydantic to define a schema for our payload. This will restrict the user to follow the schema and he cannot send any garbage value in the POST Body.
    # post_dict = post.dict()
    # post_dict["id"] = len(my_posts) + 1
    # my_posts.append(post_dict)
    # using SQL
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # using SQLAlchemy
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"status": "success", "status_code": status.HTTP_201_CREATED, "error": False,  "message": "New post created successfully", "data": new_post}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    # post = find_post(id)
    # if not post:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"status": "error", "code": 404, "error": True,  "message": f"Post with ID {id} not found", "data": {}}
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with ID {id} not found")
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    return {"status": "success", "status_code": status.HTTP_200_OK, "error": False,  "message": "Post fetched successfully", "data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with ID {id} not found")
    # my_posts.pop(index)
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    return {"status": "success", "status_code": status.HTTP_204_NO_CONTENT, "error": False,  "message": "Post deleted successfully", "data": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Post with ID {id} not found")
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} does not exist")
    return {"status": "success", "status_code": status.HTTP_200_OK, "error": False,  "message": "Post updated successfully", "data": updated_post}
