from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path, Request, status
from starlette import status
from ..models import Todos
from ..db.db import DB_ANNOTATED
from ..validation.todo_request import TodoRequest
from ..routers.auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

template = Jinja2Templates(directory='project_3/templates')

router = APIRouter(
  prefix='/todos',
  tags=['todos']
)

USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]

def redirect_to_login():
  redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
  redirect_response.delete_cookie(key='access_token')
  return redirect_response
### Pages ###

@router.get('/todo-page')
async def render_todo_page(request: Request, db: DB_ANNOTATED):
  try:
    user = await get_current_user(request.cookies.get('access_token'))
    if user is None:
      return redirect_to_login()

    todos = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

    return template.TemplateResponse('todo.html', { 'request': request, 'todos': todos, 'user': user})
  except:
    redirect_to_login()

@router.get('/add-todo-page')
async def render_add_todo_page(request: Request):
  user = await get_current_user(request.cookies.get('access_token'))
  if user is None:
      return redirect_to_login()
  return template.TemplateResponse('add-todo.html', { 'request': request })

@router.get('/edit-todo-page/{id}')
async def render_edit_todo_page(request: Request, db: DB_ANNOTATED, id: int = Path(gt=0)):
  try:
    user = await get_current_user(request.cookies.get('access_token'))
    if user is None:
      return redirect_to_login()

    todo = db.query(Todos).filter(Todos.id == id).first()

    if todo is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found' )

    return template.TemplateResponse('edit-todo.html', { 'request': request, 'todo': todo, 'user': user })
  except:
    redirect_to_login()

### Endpoints ###

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