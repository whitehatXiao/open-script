# main.py
from fastapi import FastAPI, Request
from trigger.routers import script_router, user_router
from type.api_response import ApiResponse
import uvicorn

app = FastAPI()
# 注册路由
app.include_router(script_router.router)
app.include_router(user_router.router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return ApiResponse(
        code=500,
        message=f"Server Error: {str(exc)}"
    ).to_response()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0" ,reload=True, port=8000) # 采用docker 部署时，要设置host 为0.0.0.0，否则将无法接入


