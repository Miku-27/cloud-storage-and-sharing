import jwt
from datetime import datetime,timezone,timedelta
from sqlalchemy.exc import SQLAlchemyError
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes
from app.models.model import UsersTable
from app.config import get_config

from hashlib import sha256
from secrets import compare_digest

def _generate_access_token(JWT_SECRET:str,EXPIRE_TIME:int,JWT_ALGORITHMN:str,data:str):
    now = datetime.now(timezone.utc)
    payload = {
        "sub":data,
        "iat":int(now.timestamp()),
        "exp":int((now+timedelta(minutes=EXPIRE_TIME)).timestamp())
    }

    token = jwt.encode(payload,JWT_SECRET,JWT_ALGORITHMN)

    return token


def _hash_password(plain_pass):
    return sha256(plain_pass.encode()).hexdigest()


def _verify_password(db,email,plain_password):
    hashed_key =  _hash_password(plain_key=plain_password)
    record = db.query(UsersTable.hashed_password).filter(UsersTable.email == email).first()
    if not record:
        raise ServiceException(ResultCodes.INVALID_CREDENTIALS)

    hashed_key = _hash_password(plain_password)
    is_verified = True if compare_digest(record.apikey_hash,hashed_key) else None
    if is_verified:
        return record.id
    
    raise ServiceException(ResultCodes.INVALID_CREDENTIALS)

def register_user_service(db,user_dict):
    try:
        user = db.query(UsersTable.id).filter(UsersTable.email==user_dict["email"]).first()
        if user:
            raise ServiceException(ResultCodes.USER_ALREADY_EXISTS)
        
        hashed_password = _hash_password(user_dict['password'])
        new_user = UsersTable(
            email=user_dict['email'],
            username=user_dict['username'],
            hashed_password=hashed_password,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "success":True,
            "code":ResultCodes.USER_REGISTERED,
            "data":{"id":new_user.id}
        }
    except SQLAlchemyError as se:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)
    
def login_user_service(db,user_dict):
    try:
        user_id = _verify_password(db,user_dict["email"],user_dict["password"])

        config = get_config()
        access_token = _generate_access_token(config.jwt_secret,config.access_token_expire_minute,config.jwt_algo,user_id)
        return access_token
    except SQLAlchemyError as se:

        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)
    
def change_password_service(db,user_dict,user_id):
    try:    
        user = db.query(UsersTable).filter(UsersTable.id==user_id).first()
        if not user:
            raise ServiceException(ResultCodes.USER_NOT_FOUND)

        hashed_password = _hash_password(user_dict['new_password'])
        user.hashed_password=hashed_password

        db.commit()
        return{
            'success':True,
            'code':ResultCodes.PASSWORD_UPDATED,
            'data':None
        }
    except SQLAlchemyError as se:
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)
    
