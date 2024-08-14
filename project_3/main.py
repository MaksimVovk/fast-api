from fastapi import FastAPI

from .models import Base
from .database import engine

from .routers import (
  auth, todo, admin, users
)

app = FastAPI()

@app.get('/healthy')
def heath_check():
  return { 'status': 'Healthy'}

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todo.router)
app.include_router(admin.router)
app.include_router(users.router)
