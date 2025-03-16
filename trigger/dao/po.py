from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60))  # BCrypt加密（固定60字符）
    role = Column(String(10), default="user")  # 角色字段 普通用户 user、管理员 admin
    created_time = Column(DateTime, default=datetime.utcnow)
    updated_time = Column(DateTime, default=datetime.utcnow)

# class Script(Base): TODO 脚本权限暂时先不做
#     __tablename__ = "scripts"
#     id = Column(String(36), primary_key=True)  # UUID
#     user_id = Column(Integer)
#     content = Column(String(1024))  # 脚本内容
#     is_public = Column(bool, default=False)  # 公开权限