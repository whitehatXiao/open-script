# main.py
from fastapi import FastAPI, Request
from app.logger import log_manager, log
from trigger.routers import script_router
import uvicorn
from type.constants import Constants
app = FastAPI()
# 注册路由
app.include_router(script_router.router)

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    # 绑定请求ID
    log_manager.bind_request_id(request)

    # 记录请求信息
    log.info(f"Request: {request.method} {request.url}")

    try:
        response = await call_next(request)
        log.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        log.error(f"Error: {str(e)}")
        raise


def test():
    log.info(f"Constants.PROJECT_ROOT: {Constants.PROJECT_ROOT}")
    log.info(f"Constants.PLUGIN_DIR: {Constants.PLUGIN_DIR}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000)


