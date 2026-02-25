from pydantic import BaseModel, EmailStr,Field
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

class FilesModel(BaseModel):
    files:list[FileCreateModel]=Field(min_length=1,max_length=10)


class FileUpdateModel(BaseModel):
    filename:str | None 
    status: FileStatus | None

class FileFilters(BaseModel):
    limit:int = Field(9,lt=20)
    page:int = 1