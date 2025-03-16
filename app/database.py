# /app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 仅需基础配置
Base = declarative_base()
engine = create_engine("sqlite:///./open-script.db")  # 单文件嵌入式数据库
Session = sessionmaker(bind=engine)

def get_session():
    """生成轻量级会话（无事务控制）"""
    return Session()