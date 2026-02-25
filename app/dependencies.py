from fastapi import Depends,Request,Header,Cookie
from app.config import get_config
import jwt
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes

def validate_jwt(
        request:Request,
        access_token:str=Cookie(None),
        csrf_token:str=Cookie(None),
        x_csrf_token: str = Header(None)
    ):
    try:
        if not access_token:
            raise ServiceException(ResultCodes.TOKEN_INVALID)
        payload = jwt.decode(
            access_token,
            get_config().jwt_secret,
            algorithms=[get_config().jwt_algo],
        )
    except jwt.ExpiredSignatureError as e:
        raise ServiceException(ResultCodes.TOKEN_EXPIRED) from e
    except jwt.InvalidTokenError as e:
        raise ServiceException(ResultCodes.TOKEN_INVALID) from e

    user_id = payload.get("sub")
    if not user_id:
        raise ServiceException(ResultCodes.TOKEN_PAYLOAD_INVALID)
    

    if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        if not x_csrf_token != csrf_token:
            raise ServiceException(ResultCodes.CSRF_FAILURE)
        
    return int(user_id)