# api/routers/script_router.py
from fastapi import APIRouter, UploadFile, File
from app.plugin_loader import PluginLoader, Path
from app.logger import log
import shutil
from type.apiResponse import ApiResponse
from type.constants import Constants

router = APIRouter(
    prefix="/scripts",
    tags=["脚本管理"],
    responses={404: {"description": "Not found"}}
)

plugin_loader = PluginLoader()

@router.post("/upload",
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
        return ApiResponse(
            code=200,
            data={
                "status": "loaded" if success else "failed"
            },
            message= "loaded" if success else "failed"
        )

    except Exception as e:
        log.error(f"上传失败: {str(e)}")
        return ApiResponse(
            code=500,
            message="文件操作异常"+str(e)
        )

@router.post("/execute/{script_name}",
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
        return ApiResponse(
            code=200,
            data={
                "result": result
            },
            message="脚本执行成功"
        )
    except Exception as e:
        log.error(f"执行失败: {script_name} - {str(e)}")
        return ApiResponse(
            code=500,
            message="error"+str(e)
        )


@router.get("/query",
            summary="获取已加载脚本列表",
            responses={
                200: {"description": "成功返回脚本列表"},
                500: {"description": "服务端数据加载异常"}
            })
def get_loaded_scripts():
    """获取当前已加载的所有脚本名称"""
    try:
        # 假设 plugin_loader.modules 结构为 {模块名: 模块对象}
        loaded_scripts = list(plugin_loader.modules.keys())
        log.info(f"成功获取已加载脚本列表，数量：{len(loaded_scripts)}")
        return ApiResponse(
            code=200,
            data={
                "count": len(loaded_scripts),
                "scripts": loaded_scripts
            },
            message="获取已加载脚本列表成功"
        )
    except AttributeError as e:
        log.error(f"模块属性不存在: {str(e)}")
        return ApiResponse(
            code=500,
            message="模块加载器未初始化"+str(e)
        )
    except Exception as e:
        log.error(f"获取脚本列表异常: {str(e)}")
        return ApiResponse(
            code=500,
            message="获取已加载脚本列表失败"+str(e)
        )
