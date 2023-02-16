import uvicorn
from fastapi import FastAPI, Depends
from wattpad_scraper import Wattpad
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

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


class Search_Arguments:
    
    def __init__(self, completed: Optional[bool] = True, mature:  Optional[bool] = True,
                        free:  Optional[bool] = True, paid:  Optional[bool] = True,
                        start : Optional[int] = 0 , limit:  Optional[int] = 10):
        self.completed = completed
        self.mature = mature
        self.free = free
        self.paid = paid
        self.start = start
        self.limit = limit


@app.post("/search/{query}")
async def search(query,params: Search_Arguments = Depends(Search_Arguments)):
    result = wattped.search_books(query,
                                completed=params.completed,mature=params.mature,
                                free=params.free,paid=params.paid,
                                start=params.start,limit=params.limit)
    return result


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, port=8000)