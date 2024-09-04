import uvicorn
from fastapi import FastAPI
from wattpad_scraper import Wattpad
from typing import Optional
import os
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.storage import FileBin, delete_file
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


UPLOAD_DIRECTORY = "/tmp/uploads"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
    

@app.get("/")
async def root():
    result = {"message": "Hello World! Welcome to the WattPad Extension"}
    return result


@app.get("/get/book/{book_url}")
async def get_book_url(book_url):
    result = wattped.get_book_by_url("https://www.wattpad.com/story/" + book_url)
    return result


class search_params(BaseModel):
    completed: Optional[bool] = True
    mature: Optional[bool] = True
    free: Optional[bool] = True
    paid: Optional[bool] = True
    start: Optional[int] = 0
    limit: Optional[int] = 10

class book_params(BaseModel):
    url: Optional[str]

@app.post("/search/{query}")
async def search(query: str, search_params: search_params):
    result = wattped.search_books(query,
                                completed=search_params.completed,mature=search_params.mature,
                                free=search_params.free,paid=False,
                                start=search_params.start,limit=search_params.limit)
    return result

@app.post("/book/download")
async def download_book(book_params: book_params):
    wt = Wattpad()
    book = wt.get_story(book_params.url)
    # headers = {'Content-Disposition': f'attachment; filename="{book.title}"'}
    file_path = book.save(loc=UPLOAD_DIRECTORY)
    filebin = FileBin(file_path)
    download_url = filebin.upload()
    if download_url:
        print(f"Download URL: {download_url}")

    delete_file(file_path)
    return {
        "url": download_url
    }


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, port=8000)