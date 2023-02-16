import uvicorn
from fastapi import FastAPI, Depends
from wattpad_scraper import Wattpad
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
wattped = Wattpad()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    result = {"message": "Hello World! Welcome to the WattPad Extension"}
    return result


@app.get("/get/book/{book_url}")
async def get_book_url(book_url):
    result = wattped.get_book_by_url("https://www.wattpad.com/story/" + book_url)
    return result


class params(BaseModel):
    completed: Optional[bool] = True
    mature: Optional[bool] = True
    free: Optional[bool] = True
    paid: Optional[bool] = True
    start: Optional[int] = 0
    limit: Optional[int] = 10



@app.post("/search/{query}")
async def search(query, params: params):
    print(params.json())
    result = wattped.search_books(query,
                                completed=params.completed,mature=params.mature,
                                free=params.free,paid=params.paid,
                                start=params.start,limit=params.limit)
    return result


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, port=8000)