from fastapi import APIRouter,Depends
from app.models.pydantic_models import RegisterModel,LoginModel,ChangePasswordModel
from app.services.auth_service import register_service 
from app.models.database import get_db

auth_router = APIRouter()

@auth_router.post("/user")
async def register_route(user_cred:RegisterModel,db:Session = Depends(get_db)):
    

@auth_router.patch("/user")
async def change_password_route(new_cred:ChangePasswordModel):
    pass

@auth_router.post("/token")
async def login_route(user_cred:LoginModel):
    pass