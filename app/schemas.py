from pydantic import BaseModel  # schema


class Post(BaseModel):  # define the schema for our POST Body
    title: str
    content: str
    published: bool = True
