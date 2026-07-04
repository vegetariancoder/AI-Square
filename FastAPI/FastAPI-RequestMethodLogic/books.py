from typing import Any

from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


################ GET METHODS ################
@app.get("/")
async def homepage() -> dict:
    return {"message": "Home Page"}

@app.get("/read_all_books")
async def read_all_books() -> list[dict]:
    return BOOKS

# path parameter
@app.get("/read_book/{book_title}")
async def get_book_by_title(book_title: str) -> dict:
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


# query parameter
@app.get("/read_book_by_category/")
async def get_book_by_category(category: str)-> list[Any] | dict[str, str]:
    all_books = []
    for book in BOOKS:
        if book.get('category') == category:
            all_books.append(book)
    if len(all_books) > 0:
        return all_books
    else:
        return {"message": "No books found in this category"}

# path parameter with query parameter

@app.get("/read_book_by_title_and_category/{book_title}/")
async def get_author_by_title_and_category(book_title: str, category: str) -> list[Any] | dict[str, str]:
    books_to_return = []
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold() and book.get("category") == category:
            books_to_return.append(book)
    if len(books_to_return) > 0:
        return books_to_return
    return {"message": "No books found with this title and category"}

################ POST METHODS ################

@app.post("/create_book/")
async def create_book(book: dict):
    BOOKS.append(book)
    return {"message": "Book created successfully"}

############### PUT METHODS ################
@app.put("/update_book/{title}/")
async def update_book(title: str, new_title: str):
    for books in BOOKS:
        if books.get("title") == title:
            books["title"] = new_title
    return {"message": "Book updated successfully"}

################ DELETE METHODS ################
@app.delete("/delete_book/{title}/")
async def delete_book(title: str):
    for books in BOOKS:
        if books.get("title") == title:
            BOOKS.remove(books)
    return {"message": "Book deleted successfully"}


############### ASSIGNMENT ####################

@app.get("/get_book_by_author/{author_name}/")
async def get_book_by_author(author_name: str) -> list[Any] | dict[str, str]:
    all_books = []
    for book in BOOKS:
        if book.get('author') == author_name:
            all_books.append(book)
    if len(all_books) > 0:
        return all_books
    return {"message": "Book not found"}


if __name__ == "__main__":
    uvicorn.run("books:app", host="127.0.0.1", port=8000, reload=True)