from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class DeveloperSetting(BaseSettings):
    database_uri:str 
    jwt_secret:str
    jwt_algo:str
    access_token_expire_minute:int
    cookie_secure:bool=False
    cookie_samesite:str="lax"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix=""
    )


#singleton pattern
@lru_cache
def get_config():
    devSetting = DeveloperSetting()
    return devSetting

    