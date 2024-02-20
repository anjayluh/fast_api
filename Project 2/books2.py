from typing import Optional
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        description: str,
        rating: int,
        published_date: int,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(None, title="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Sample book",
                "author": "Username",
                "description": "Sample book description",
                "rating": 5,
                "published_date": 2024,
            }
        }


BOOKS = [
    Book(1, "Computer Science", "Author one", "description one", 5, 2024),
    Book(2, "Computer Vision", "Author two", "description two", 3, 2020),
    Book(3, "Computer Science", "Author three", "description three", 5, 2024),
    Book(4, "Computer Science", "Author four", "description four", 4, 2021),
    Book(5, "Computer Science", "Author five", "description five", 1, 2022),
    Book(6, "Computer Science", "Author six", "description six", 5, 2024),
    Book(7, "campus north", "Author two", "description nine", 3, 2022),
    Book(8, "Engineer", "Author four", "description seven", 4, 2019),
]


@app.get("/books")
def get_books():
    return BOOKS


def get_book_id():
    id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return id


@app.post("/books/create", status_code=status.HTTP_201_CREATED)
def add_book(values: BookRequest):
    values.id = get_book_id()
    new_book = Book(**values.model_dump())
    BOOKS.append(new_book)


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
def filter_by_rating(book_rating: int = Query(gt=-1, lt=6)):
    result = []
    for book in BOOKS:
        if book.rating == book_rating:
            result.append(book)

    return result


@app.get("/books/published_date/", status_code=status.HTTP_200_OK)
def filter_by_published_date(published_date: int):
    result = []
    for book in BOOKS:
        if book.published_date == published_date:
            result.append(book)

    return result


@app.put("/books/update_book", status_code=status.HTTP_200_OK)
def update_book(updated_book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == updated_book.id:
            BOOKS[i] = updated_book


@app.delete("/books/", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            index = BOOKS.index(book)
            BOOKS.pop(index)
            return
    raise HTTPException(status_code=404, detail="Book not found")
