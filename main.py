from fastapi import FastAPI, UploadFile, File, Request
from core.plugin_loader import PluginLoader,Path
from core.logger import log_manager, log
import shutil

app = FastAPI()
plugin_loader = PluginLoader()

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000)


@app.post("resources/upload/")
async def upload_script(file: UploadFile = File(...)):
    # 保存到 scripts 目录
    script_path = Path("resources/upload/scripts") / file.filename
    with open(script_path, "wb") as buffer:
        buffer.write(await file.read())

    # 复制到 plugins 目录并加载
    plugin_path = Path("resources/upload/plugins") / file.filename
    shutil.copy(script_path, plugin_path)
    success = plugin_loader.load_plugin(script_path.stem)
    return {"status": "loaded" if success else "failed"}

@app.post("/execute/")
def execute_script(script_name: str):
    log.info(f"Executing script: {script_name}")
    try:
        result = plugin_loader.run_plugin(script_name)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

