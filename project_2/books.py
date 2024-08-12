from fastapi import FastAPI, Body, Path, Query, HTTPException
from models.books import CreateBookRequest
from starlette import status

app = FastAPI()

class Book:
  id: int
  title: str
  author: str
  description: str
  rating: int
  published_date: int

  def __init__(self, id, title, author, description, rating, published_date):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating
    self.published_date = published_date

BOOKS = [
  Book(
    id=1,
    title='The Hidden Language of Computer Hardware and Software',
    author='Charl Petzold',
    description='Computers',
    rating=5,
    published_date=2012,
  ),
  Book(
    id=2,
    title='Computer Hardware',
    author='Charly Petzold',
    description='Hardware',
    rating=4,
    published_date=2012,
  ),
  Book(
    id=3,
    title='Computer Software',
    author='Charles Petzold',
    description='Software',
    rating=5,
    published_date=2012,
  ),
]

@app.get('/books', status_code=status.HTTP_200_OK)
async def get_books():
  return BOOKS

@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
  for b in BOOKS:
    if b.id == book_id:
      return b

  raise HTTPException(status_code=404, detail='Item not found')

@app.get('/books/', status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(gt=0, lt=6)):
  books = []

  for book in BOOKS:
    if book.rating == rating:
      books.append(book)

  return books

@app.post('/books/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(data: CreateBookRequest):
  book = Book(**data.dict())

  BOOKS.append(find_book_id(book))

  return { "message": "Book created"}

@app.put('/books/update-book', status_code=status.HTTP_204_NO_CONTENT)
async def update_book (book : CreateBookRequest):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book.id:
      BOOKS[i] = book

@app.delete('/books/delete-book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book (book_id: int = Path(gt=0)):
  for i in range(len(BOOKS)):
    if BOOKS[i].id == book_id:
      BOOKS.pop(i)
      break

@app.get('/books/by-year/', status_code=status.HTTP_200_OK)
async def get_book_by_year(date: int = Query(gt=1900, lt=2031)):
  books = []
  try:
    for b in BOOKS:
      if b.published_date == date:
        books.append(b)
  except Exception as e:
    print(e)
  return books

def find_book_id(book: Book):
  if len(BOOKS) > 0:
    book.id = BOOKS[-1].id + 1
  else:
    book.id = 1

  return book