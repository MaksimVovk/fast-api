from pydantic import BaseModel

class CreateUserRequest(BaseModel):
  email: str
  username: str
  firstname: str
  lastname: str
  password: str
  is_active: bool = True
  role: str
  phone_number: str

class Token(BaseModel):
  access_token: str
  token_type: str

class ChangePassword(BaseModel):
  password: str

class UpdatePhone(BaseModel):
  phone: str