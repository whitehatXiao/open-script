from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(
                String(36),
                unique=True,
                index=True,  # 添加索引提升查询效率
                server_default=str(uuid.uuid4()),  # 服务端生成默认值 UUID唯一标识主键
                nullable=False )
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