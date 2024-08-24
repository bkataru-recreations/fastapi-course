from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "me"}}


@app.get("/blog")
def blog(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return "hello"
    else:
        return {"data": "aaa"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "unpublished"}


@app.get("/blog/{id}")
def about(id: int):
    return {"name": id}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog/create")
def create(blog: Blog):
    print(blog)
    return blog


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="127.0.0.1", port=8000)
