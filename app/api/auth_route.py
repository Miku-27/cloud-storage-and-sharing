from fastapi import APIRouter
from app.models.pydantic_models import RegisterModel,LoginModel
auth_router = APIRouter()

@auth_router.post("/user")
async def register_route(user_cred:RegisterModel):
    pass

@auth_router.patch("/user")
async def change_password_route(new_cred:ChangePassword):
    pass

@auth_router.post("/token")
async def login_route(user_cred:LoginModel):
    pass