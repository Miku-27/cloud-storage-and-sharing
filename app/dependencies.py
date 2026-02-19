from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials,APIKeyCookie
from fastapi import Depends
from app.config import get_config
import jwt
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes

cookie_data = APIKeyCookie(name="access_token", auto_error=False)

def validate_jwt(token:str = Depends(cookie_data)):
    try:
        if not token:
            raise ServiceException(ResultCodes.TOKEN_INVALID)
        payload = jwt.decode(
            token,
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
    
    return int(user_id)