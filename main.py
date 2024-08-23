from fastapi import FastAPI
from fastapi.params import Body

app=FastAPI() #initializing the FastAPI instance

@app.get("/") #decorator. This contains the FastAPI instance and the path to be accessed. It can either be called an API route or Path Operation.
async def root(): #function. The async keywork is optional, it is used to indicate that the function is asynchronous, i.e., communicating with the Database, etc.
    return {"status": "success", "code": 200, "error": False,  "message": "API is working!", "data": {}}

@app.get("/posts")
def get_posts():
    return {"status": "success", "code": 200, "error": False,  "message": "These are your posts", "data": [{"title": "Post 1", "content": "This is post 1"}, {"title": "Post 2", "content": "This is post 2"}, {"title": "Post 3", "content": "This is post 3"}]}

@app.post("/create_post")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"status": "success", "code": 200, "error": False,  "message": "New post created successfully", "data": payload}