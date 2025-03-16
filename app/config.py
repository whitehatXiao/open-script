# app/config.py
import os
from datetime import timedelta

class Settings:

    # JWT 加密密钥设置
    SECRET_KEY = os.getenv("SECRET_KEY", "whitehatxiao@outlook.com")  # 生产环境务必替换为随机字符串
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    # TODO


settings = Settings()
