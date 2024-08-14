from typing import Annotated
from ..database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

DB_ANNOTATED = Annotated[Session, Depends(get_db)]
