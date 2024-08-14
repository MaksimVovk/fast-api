from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException
from ..validation.users import CreateUserRequest, Token
from ..models import Users
from starlette import status
from ..db.db import DB_ANNOTATED
from typing import Annotated, Optional
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError # type: ignore

router = APIRouter(
  prefix='/auth',
  tags = ['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

DB_ANNOTATED_AUTH = Annotated[OAuth2PasswordRequestForm, Depends()]
DB_ANNOTATED_BEARER = Annotated[str, Depends(oauth2_bearer)]
SECRET_KEY = '25fd775657d238053357080198e3eed94e96ce522a1b593fc520276022324cdf'
ALGORITHM = 'HS256'

def auth_user(username: str, password: str, db):
  user = db.query(Users).filter(Users.username == username).first()
  if not user:
    return False

  if not bcrypt_context.verify(password, user.password):
    return False

  return user

def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta):
  encode = {
    'sub': username,
    'id': user_id,
    'role': role,
  }
  exp = datetime.now(timezone.utc) + expires_delta
  encode.update({'exp': exp})

  return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: DB_ANNOTATED_BEARER):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: Optional[str] = payload.get('sub')
    user_id: Optional[int] = payload.get('id')
    role: Optional[str] = payload.get('role')
    if username is None or user_id is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    return { 'username': username, 'user_id': user_id, 'role': role }

  except JWTError as e:
    print(e)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired.')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: DB_ANNOTATED, request: CreateUserRequest):
  create_user_model = Users(
    email=request.email,
    username=request.username,
    firstname=request.firstname,
    lastname=request.lastname,
    role=request.role,
    password=bcrypt_context.hash(request.password),
    is_active=request.is_active,
    phone_number=request.phone_number
  )

  db.add(create_user_model)
  db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(
  form_data: DB_ANNOTATED_AUTH,
  db: DB_ANNOTATED
):
  user = auth_user(username=form_data.username, password=form_data.password, db=db)

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

  payload = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=20))
  return {
    'access_token': payload,
    'token_type': 'bearer'
  }