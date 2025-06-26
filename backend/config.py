from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "mysql+pymysql://cG5sdmqlmmFdr4Bdma8W09iI:Z8LkJLc796OhatjZSj77keT2NN9uXE@dpshmy-etejt5urwv2osw0y-pub.proxy.dms.aliyuncs.com:3306/grading?charset=utf8mb4"
    
    # JWT配置
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 微信小程序配置
    wechat_app_id: str = "wx90cd6358a941cb7a"
    wechat_app_secret: str = "412dcaf89481e2168186598f4f2c1420"
    
    class Config:
        env_file = ".env"

settings = Settings() 