from fastapi import (
  FastAPI, Body
)

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get('/books')
async def get_books():
  return BOOKS

@app.get('/books/{title}')
async def get_book(title: str):
  for book in BOOKS:
    if book.get('title').lower() == title.lower():
      return book
    else:
      return { 'message': 'Book not found'}

@app.get('/books/')
async def get_book_by_category(category: str):
  books = []
  for book in BOOKS:
    if book.get('category').lower() == category.lower():
      books.append(book)

  return books

@app.get('/books/{author}/')
async def get_book_by_author(author: str, category: str):
  books = []
  for book in BOOKS:
    isAuthor = book.get('author').lower() == author.lower()
    isCategory = book.get('category').lower() == category.lower()
    if isAuthor and isCategory:
      books.append(book)

  return books

@app.post('/books/create-book')
async def create_book(book = Body()):
  BOOKS.append(book)
  return { "message": "book created" }

@app.put('/books/update-book')
async def update_book(book = Body()):
  # book = next(b for b in BOOKS if b.get('title').lower() == book.get('title').lower())
  for i in range(len(BOOKS)):
    if BOOKS[i].get('title').lower() == book.get('title').lower():
      BOOKS[i] = book
  return { "message": "book updated" }

@app.delete('/books/delete-book/{title}')
async def delete_book(title: str):
  for i in range(len(BOOKS)):
    try:
      if BOOKS[i].get('title').casefold() == title.casefold():
        BOOKS.pop(i)
    except Exception as e:
      print(i)
  return { "message": "book deleted" }

@app.get('/books/assigment/{author}')
async def get_books_by_author(author: str):
  books = list(filter(lambda book: book.get('author').lower() == author.lower(), BOOKS))

  return books