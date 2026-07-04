from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
import uvicorn
from pydantic import BaseModel, Field
from starlette import status

# define the app
app = FastAPI()

# create the book object
class Book():
    book_id : int
    title : str
    author : str
    description : str
    rating : int
    publication_date : int
    publish_month : str

    def __init__(self, book_id, title, author, description, rating, publication_date, publish_month):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publication_date = publication_date
        self.publish_month = publish_month

# create the book request object using pydantic
class BookRequest(BaseModel):
    book_id: Optional[int] = Field(description='ID is not needed on create', default=None,gt=0)
    title: str = Field(description='Title is required', min_length=3)
    author: str = Field(description='Author is required', min_length=3)
    description: str = Field(description='Description is required', min_length=5, max_length=200)
    rating: int = Field(description='Rating is required', gt=0, lt=6)
    publication_date: int = Field(description='Publication date is required', gt=2000, lt=2099)
    publish_month: str = Field(description='Publish month is required in Abbreviated Format', min_length=3, max_length=3)

    model_config = {
        'json_schema_extra': {
            'example': {
                'title': 'A New Book',
                'author': 'Sahil',
                'description': 'Go with all your heart and mind',
                'rating': 5,
                'publication_date': 2023,
                'publish_month': 'Jan'
            }
        }
    }


books = [
    Book(1, "Book 1", "Author 1", "Description 1", 5, 2023,publish_month="Jan"),
    Book(2, "Book 2", "Author 2", "Description 2", 4, 2022,publish_month="Feb"),
    Book(3, "Book 3", "Author 3", "Description 3", 3, 2021,publish_month="Mar"),
    Book(4, "Book 4", "Author 4", "Description 4", 2, 2020,publish_month="Apr"),
    Book(5, "Book 5", "Author 5", "Description 5", 1, 2019,publish_month="May"),
]


# get all books
@app.get("/all_books", status_code=status.HTTP_200_OK)
async def get_all_books():
    return books

@app.get("/all_books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    book_by_id = []
    for book in books:
        if book.book_id == book_id:
            book_by_id.append(book)
    if len(book_by_id) > 0:
        return book_by_id
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/all_books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(gt=0)):
    book_by_rating = []
    for book in books:
        if book.rating == rating:
            book_by_rating.append(book)
    if len(book_by_rating) > 0:
        return book_by_rating
    raise HTTPException(status_code=404, detail="Book not found")


def allot_book_id(book : Book):
    book.book_id = books[-1].book_id + 1 if books else 1
    return book

@app.post("/all_books/create_book", status_code=status.HTTP_201_CREATED)
async def add_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(allot_book_id(new_book))
    return {"message": "Book created successfully"}

@app.put("/all_books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request : BookRequest):
    book_change = False
    for book in books:
        if book.book_id == book_request.book_id:
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            book.publication_date = book_request.publication_date
            return {"message": "Book updated successfully"}
    if not book_change:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/all_books/delete_book/{book_id}")
async def delete_book(book_id: int = Path(gt=0, lt=len(books)+1)):
    for book in books:
        if book.book_id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")



if __name__ == "__main__":
    uvicorn.run("books_2:app", host="127.0.0.1", port=8000, reload=True)