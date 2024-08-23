from fastapi import FastAPI

app=FastAPI()

@app.get("/")
async def root():
    print("API is working!")
    return {"message": "API is working!"}