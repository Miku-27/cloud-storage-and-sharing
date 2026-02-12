from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends
from app.config import get_config
import jwt
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes


security = HTTPBearer()

def validate_jwt(cred:HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            cred.credentials,
            get_config().jwt_secret,
            algorithms=[get_config().jwt_algo],
        )
    except jwt.ExpiredSignatureError:
        raise ServiceException(ResultCodes.TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        raise ServiceException(ResultCodes.TOKEN_INVALID)

    user_id = payload.get("sub")
    if not user_id:
        raise ServiceException(ResultCodes.TOKEN_PAYLOAD_INVALID)
    
    return user_id