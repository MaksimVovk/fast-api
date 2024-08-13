# Here is your opportunity to keep learning!

# 1. Create a new route called Users.

# 2. Then create 2 new API Endpoints

# get_user: this endpoint should return all information about the user that is currently logged in.

# change_password: this endpoint should allow a user to change their current password.

from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import Annotated
from models import Users
from db.db import DB_ANNOTATED
from routers.auth import get_current_user
from validation.users import ChangePassword, UpdatePhone
from passlib.context import CryptContext

router = APIRouter(
  prefix='/user',
  tags=['user']
)

USER_DEPENDENCY = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED
):
  if user is None or user.get('user_id') is None:
    raise HTTPException(status_code=401, detail='Authentication failed')
  try:
    user_data = db.query(Users).filter(Users.id == user.get('user_id')).first()

    current_user = {
      'id': user_data.id,
      'email': user_data.email,
      'username': user_data.username,
      'lastname': user_data.lastname,
      'firstname': user_data.firstname,
      'role': user_data.role,
      'is_active': user_data.is_active,
      'phone_number': user_data.phone_number,
    }
    return current_user
  except Exception as e:
    print(e)

@router.put('/change-password/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  body: ChangePassword,
  id: int = Path(gt=0),
):
  if user is None or user.get('user_id') is None:
    raise HTTPException(status_code=401, detail='Authentication failed')

  user_model = db.query(Users).filter(Users.id == id).first()

  if user_model is None:
    raise HTTPException(status_code=404, detail='Item not found')

  user_model.password = bcrypt_context.hash(body.password)
  db.commit()

@router.put('/update-phone/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_phone(
  user: USER_DEPENDENCY,
  db: DB_ANNOTATED,
  body: UpdatePhone,
  id: int = Path(gt=0)
):
  if user is None or user.get('user_id') is None:
    raise HTTPException(status_code=401, detail='Authentication failed')

  user_model = db.query(Users).filter(Users.id == id).first()

  if user_model is None:
    raise HTTPException(status_code=404, detail='Item not found')

  user_model.phone_number = body.phone
  db.commit()