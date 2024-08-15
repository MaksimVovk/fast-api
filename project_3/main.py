from fastapi import FastAPI, Request, status

from .models import Base
from .database import engine

from .routers import (
  auth, todo, admin, users
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get('/healthy')
def heath_check():
  return { 'status': 'Healthy'}

Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='project_3/static'), name='static')

@app.get('/')
def test(request: Request):
  return RedirectResponse(url='/todos/todo-page')

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)
