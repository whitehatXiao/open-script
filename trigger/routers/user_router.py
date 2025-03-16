# trigger/routers/user_router.py
from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from app.logger import log

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_session
from trigger.dao.po import User
from type.api_response import ApiResponse
import bcrypt
from pydantic import BaseModel
from app.config import settings  # 导入配置
from app.security import get_current_user



router = APIRouter(
    prefix="/users",
    tags=["用户管理"],
    # responses={
    #     400: {"model": ApiResponse, "description": "请求参数错误"},
    #     500: {"model": ApiResponse, "description": "服务端内部错误"}
    # }
)

# 请求体模型（仅需用户输入字段）
class UserCreate(BaseModel):
    username: str
    password: str  # 接收明文密码，服务端加密

@router.post("/register",
             summary="用户注册",
             response_model=None  # 显式禁用响应模型
             )
async def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    """注册新用户（自动加密密码）"""
    try:
        # 检查用户名是否存在
        if db.query(User).filter(User.username == user_data.username).first():
            return ApiResponse(
                code=400,
                message="用户名已存在"
            )

        log.info(f"正在注册用户：{user_data.username}")
        # BCrypt 加密密码（自动生成盐）
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        # 创建用户对象
        new_user = User(
            username=user_data.username,
            password_hash=hashed_password,
            role="user",  # 默认角色
        )

        # 写入数据库
        db.add(new_user)
        db.commit()
        log.info(f"用户注册成功：{user_data.username}")
        return ApiResponse(
            code=201,
            data={"user_id": new_user.id},
            message="用户注册成功"
        ).to_response()

    except IntegrityError as e:
        db.rollback()
        return ApiResponse(
            code=400,
            message="数据完整性错误（如重复用户名）"
        )
    except Exception as e:
        db.rollback()
        return ApiResponse(
            code=500,
            message=f"数据库写入失败: {str(e)}"
        )


# JWT 鉴权方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# 登录请求体
class UserLogin(BaseModel):
    username: str
    password: str

# 生成 JWT 令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

@router.post("/login",
             summary="用户登录",
             response_model=None  # 显式禁用响应模型
             )
async def login(user_data: UserLogin, db: Session = Depends(get_session)):
    log.info(f"正在登录用户：{user_data.username}")
    # 验证用户名密码
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not bcrypt.checkpw(
            user_data.password.encode('utf-8'),
            user.password_hash.encode('utf-8')
    ):
        return ApiResponse(
            code=status.HTTP_401_UNAUTHORIZED,
            message="用户名或密码错误"
        ).to_response()

    # 生成令牌
    access_token = create_access_token(
        data={"sub": user.user_id},  # 将 user_id 写入令牌
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    log.info(f"用户登录成功：{user_data.username}")
    return ApiResponse(
        code=200,
        data={"access_token": access_token, "token_type": "bearer"},
        message="登录成功"
    ).to_response()

@router.get("/me",
            summary="获取当前用户信息",
            response_model=None  # 显式禁用响应模型
            )
async def read_users_me(current_user: User = Depends(get_current_user)):
    log.info(f"正在获取用户信息：{current_user.username}")
    return ApiResponse(
        code=200,
        data={
            "user_id": current_user.user_id,
            "username": current_user.username,
            "role": current_user.role
        },
        message="成功获取用户信息"
    ).to_response()

