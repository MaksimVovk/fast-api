from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Path
from starlette import status
from ..models import Todos
from ..db.db import DB_ANNOTATED
from ..routers.auth import get_current_user

router = APIRouter(
  prefix='/admin',
  tags=['admin']
)

USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_all(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
):
  if user is None or user.get('role') != 'God':
    raise HTTPException(status_code=401, detail='Authentication failed')
  return db.query(Todos).all()

@router.delete('/todo/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: USER_DEPENDENCY,
    db: DB_ANNOTATED,
    id: int = Path(gt=0)
):
  if user is None or user.get('role') != 'God':
    raise HTTPException(status_code=401, detail='Authentication failed')

  todo_model = db.query(Todos)\
    .filter(Todos.id == id)\
    .first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')

  todo_model = db.query(Todos).filter(Todos.id == id).delete()
  db.commit()
