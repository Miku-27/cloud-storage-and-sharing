from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

class DeveloperSetting(BaseSettings):
    database_uri:str 

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix=""
    )


#singleton pattern
@lru_cache
def get_config():
    devSetting = DeveloperSetting()
    return devSetting

    