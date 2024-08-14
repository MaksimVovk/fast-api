from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path
from starlette import status
from ..models import Todos
from ..db.db import DB_ANNOTATED
from ..validation.todo_request import TodoRequest
from ..routers.auth import get_current_user

router = APIRouter(
  tags=['todo']
)

USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all(user: USER_DEPENDENCY, db: DB_ANNOTATED):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
  return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

@router.get('/todo/{id}', status_code=status.HTTP_200_OK)
async def get_todo_by_id(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  id: int = Path(gt=0)
):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
  todo_model = db.query(Todos)\
    .filter(Todos.id == id)\
    .filter(Todos.owner_id == user.get('user_id'))\
    .first()

  if todo_model is not None:
    return todo_model

  raise HTTPException(status_code=404, detail='Todo not found')

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  todo_request: TodoRequest
):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
  todo_model = Todos(**todo_request.dict(), owner_id=user.get('user_id'))

  db.add(todo_model)
  db.commit()

@router.put('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  todo_request: TodoRequest,
  id: int = Path(gt=0)
):
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
  todo_model = db.query(Todos)\
    .filter(Todos.id == id)\
    .filter(Todos.owner_id == user.get('user_id'))\
    .first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')

  todo_model.title = todo_request.title
  todo_model.description = todo_request.description
  todo_model.priority = todo_request.priority
  todo_model.complete = todo_request.complete

  db.add(todo_model)
  db.commit()

@router.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  id: int = Path(gt=0)
):
  if user is None or user.get('user_id') is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication Failed')
  todo_model = db.query(Todos)\
    .filter(Todos.id == id)\
    .filter(Todos.owner_id == user.get('user_id'))\
    .first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')

  todo_model = db.query(Todos).filter(Todos.id == id).delete()
  db.commit()