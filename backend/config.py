from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = ""
    
    # JWT配置
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 微信小程序配置
    wechat_app_id: str = ""
    wechat_app_secret: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings() 
