# /app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from type.constants import Constants
from app.logger import log

# 数据库初始化配置
Base = declarative_base()

# 导入所有模型类（必须在 create_all 前导入）
from trigger.dao.po import User

engine = create_engine("sqlite:///"+str(Constants.DEVOPS_DIR)+"/sql/open-script.db")  # 单文件嵌入式数据库
Session = sessionmaker(bind=engine)

# 此时 Base 已包含 User 类的元数据
Base.metadata.create_all(engine)
log.info("sqlite 数据库初始化成功")

def get_session():
    """生成轻量级会话（无事务控制）"""
    return Session()