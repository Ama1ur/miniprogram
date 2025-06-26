# 配置文件示例
# 请复制此文件为 config.py 并修改相应的配置

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    database_url: str = "mysql+pymysql://username:password@localhost:3306/exam_analysis"
    
    # JWT配置
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 微信小程序配置
    wechat_app_id: str = "your-wechat-app-id"
    wechat_app_secret: str = "your-wechat-app-secret"
    
    class Config:
        env_file = ".env"

settings = Settings()

# 配置说明：
# 1. 安装依赖: pip install -r requirements.txt
# 2. 配置数据库: 修改 database_url 为你的MySQL数据库连接字符串
# 3. 配置JWT密钥: 修改 secret_key 为一个强密码
# 4. 配置微信小程序: 在微信公众平台获取 app_id 和 app_secret
# 5. 运行应用: python main.py 或 uvicorn main:app --reload 