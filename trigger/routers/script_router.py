# api/routers/script_router.py
from fastapi import APIRouter, UploadFile, File
from app.plugin_loader import PluginLoader, Path
from app.logger import log
import shutil
from type.constants import Constants

router = APIRouter(
    # prefix="/scripts",
    tags=["脚本管理"],
    responses={404: {"description": "Not found"}}
)

plugin_loader = PluginLoader()

@router.post("/scripts/upload",
             summary="上传插件脚本",
             responses={
                 200: {"description": "插件加载成功"},
                 500: {"description": "文件操作异常"}
             })
async def upload_script(file: UploadFile = File(...)):
    """处理脚本上传全流程"""
    try:
        # 保存到 upload/scripts
        script_path = Constants.SCRIPTS_DIR / file.filename
        with open(script_path, "wb") as buffer:
            buffer.write(await file.read())

        # 复制到 upload/plugins
        plugin_path = Constants.PLUGIN_DIR / file.filename
        shutil.copy(script_path, plugin_path)

        success = plugin_loader.load_plugin(script_path.stem)
        return {"status": "loaded" if success else "failed"}
    except Exception as e:
        log.error(f"上传失败: {str(e)}")
        raise

@router.post("/scripts/execute/{script_name}",
             summary="执行指定脚本",
             responses={
                 404: {"description": "脚本未找到"},
                 500: {"description": "执行异常"}
             })
def execute_script(script_name: str):
    """执行已加载的脚本"""
    log.info(f"开始执行脚本: {script_name}")
    try:
        result = plugin_loader.run_plugin(script_name)
        log.info(f"脚本执行完成: {script_name}")
        return {"result": result}
    except Exception as e:
        log.error(f"执行失败: {script_name} - {str(e)}")
        return {"error": str(e)}