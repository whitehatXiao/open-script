# app/security.py
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_session
from trigger.dao.po import User
from app.config import settings
from type.api_response import ApiResponse


# OAuth2PasswordBearer 鉴权流程
# 核心作用：实现 OAuth2 密码模式的令牌提取与验证。
# 工作步骤：
# 令牌提取：自动检查请求头 Authorization: Bearer <token>，若无令牌则返回 401 错误。
# 依赖传递：通过 token: str = Depends(oauth2_scheme) 将令牌传递给后续依赖（如 get_current_user）。
# 令牌验证：在 get_current_user 中使用 jwt.decode 解码并验证令牌有效性。
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# token 令牌验证
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_session)
) -> User:
   credentials_exception = ApiResponse(
      code=status.HTTP_401_UNAUTHORIZED,
      message="无效的认证令牌",
      headers={"WWW-Authenticate": "Bearer"}
   ).to_response()

   try:
      payload = jwt.decode(
         token,
         settings.SECRET_KEY,
         algorithms=[settings.ALGORITHM]
      )
      user_id: str = payload.get("sub")
      if not user_id:
         raise credentials_exception
   except JWTError:
      raise credentials_exception

   user = db.query(User).filter(User.user_id == user_id).first()
   if not user:
      raise credentials_exception
   return user


# 实现角色校验依赖
def require_role(required_role: str):
   def role_checker(current_user: User = Depends(get_current_user)):
      if current_user.role != required_role:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
         )
      return current_user
   return role_checker
