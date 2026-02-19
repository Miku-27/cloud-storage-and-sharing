from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class DeveloperSetting(BaseSettings):
    database_uri:str 
    jwt_secret:str
    jwt_algo:str
    access_token_expire_minute:int
    cookie_secure:bool=False
    cookie_samesite:str="lax"

    storage_endpoint_url:str
    storage_region:str
    access_key_id:str
    access_key_secret:str
    bucket_name:str
    bucket_url_expire_seconds:int


    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix=""
    )


#singleton pattern
@lru_cache
def get_config():
    devSetting = DeveloperSetting()
    return devSetting

    