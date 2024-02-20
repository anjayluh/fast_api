from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Math", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
    {"title": "Title Seven", "author": "Author Two", "category": "math"},
]


@app.get("/books")
def all_books():
    return BOOKS


@app.get("/books/{dynamic_param}")
def filter_book_by_dynamic_string_property(dynamic_param: str):
    return {"dynamic_param": dynamic_param}


@app.get("/books/{book_title}")
def book_details(book_title: str):
    for book in BOOKS:
        if book.get("title").lower() == book_title:
            return book
        return {"error": "Book not found"}


@app.get("/books/")
def book_category(category: str):
    result = []
    for book in BOOKS:
        if book.get("category").lower() == category:
            result.append(book)

    return result


@app.get("/books/{author}")
def book_get_by_author_by_category(author: str, category: str):
    result = []
    for book in BOOKS:
        if (
            book.get("author").lower() == author.lower()
            and book.get("category").lower() == category.lower()
        ):
            result.append(book)

    return result


@app.get("/books/{author}/")
def book_get_by_author(author: str):
    result = []
    for book in BOOKS:
        if book.get("author").lower() == author.lower():
            result.append(book)

    return result


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/")
def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == title.casefold():
            BOOKS.pop(i)
            break
