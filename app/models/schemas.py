from pydantic import BaseModel, EmailStr
from app.models.types import FileStatus

class RegisterModel(BaseModel):
    username:str
    email:EmailStr
    password:str

class LoginModel(BaseModel):
    email:str
    password:str

class ChangePasswordModel(BaseModel):
    old_password:str
    new_password:str

class ForgotPassword(BaseModel):
    token:str
    new_password:str

class FileCreateModel(BaseModel):
    file_name:str
    file_size:int
    mime_type:str

class FileUpdateModel(BaseModel):
    filename:str | None 
    status: FileStatus | None