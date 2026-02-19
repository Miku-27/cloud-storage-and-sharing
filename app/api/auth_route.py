from fastapi import APIRouter,Depends,Response
from app.models.schemas import RegisterModel,LoginModel,ChangePasswordModel
from app.services.auth_service import register_user_service,login_user_service,change_password_service
from app.models.database import get_db
from app.utils.response import make_response
from app.config import get_config
from sqlalchemy.orm import Session
from app.dependencies import validate_jwt

auth_router = APIRouter()

@auth_router.post("/user")
async def register_route(user_cred:RegisterModel,db:Session = Depends(get_db)):
    response = register_user_service(db,user_cred.model_dump())
    return make_response(response)

@auth_router.patch("/user")
async def change_password_route(new_cred:ChangePasswordModel,db:Session = Depends(get_db),user_id=Depends(validate_jwt)):
    response = change_password_service(db,new_cred.model_dump(),user_id)
    return make_response(response)


@auth_router.post("/token")
async def login_route(api_response:Response,user_cred:LoginModel,db=Depends(get_db)):
    token = login_user_service(db,user_cred.model_dump())
    api_response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=get_config().cookie_secure,
        samesite=get_config().cookie_samesite,
        max_age=get_config().access_token_expire_minute*60
    )

    return {"success":True}

    