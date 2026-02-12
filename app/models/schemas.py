import re
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, TypeAdapter, model_validator,HttpUrl

class RegisterModel(BaseModel):
    username:str
    email:EmailStr
    passsword:str

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