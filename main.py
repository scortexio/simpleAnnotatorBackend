from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

app = FastAPI()


class Annotation(BaseModel):
    x: int
    y: int
    label: str


class Image(BaseModel):
    url: str
    annotations: List[Annotation] = []

database = [
    Image(url=f"https://picsum.photos/id/{i}/800/600")
    for i in range(20)
]

@app.get("/images")
async def images():
    return [{"id": f"{i}", "url": image.url} for i, image in enumerate(database)]


@app.get("/annotation/{id}")
async def annotations(id: str):
    image = database[int(id)]
    return image.annotations

@app.put("/annotation/{id}")
async def annotations(id: str, body: List[Annotation]):
    image = database[int(id)]
    image.annotations = body
    return Response()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
