import logging
import sys
from pathlib import Path
from contextvars import ContextVar
from loguru import logger
from fastapi import Request

class UnifiedLogger:
    """集成Uvicorn日志的Loguru配置器"""

    def __init__(self):
        self.log_dir = Path(__file__).parent.parent / "logs"
        self.request_id = ContextVar("request_id", default="SYSTEM")
        self._init_config()

    def _init_config(self):
        # 创建日志目录
        self.log_dir.mkdir(exist_ok=True)

        # 移除Loguru默认配置
        logger.remove()

        # 控制台输出配置（含Uvicorn日志）
        logger.add(
            sys.stderr,
            format=self._console_format,
            level="DEBUG",
            enqueue=True,  # 异步安全写入[3,8](@ref)
            filter=self._filter_uvicorn
        )

        # 文件输出配置
        logger.add(
            self.log_dir / "app_{time:YYYY-MM-DD}.log",
            rotation="00:00",          # 每日切割[3](@ref)
            retention="30 days",       # 保留30天[3](@ref)
            compression="zip",         # 压缩旧日志[3](@ref)
            format=self._file_format,
            level="INFO"
        )

        # 接管Python标准日志库
        self._redirect_standard_logging()

    def _redirect_standard_logging(self):
        """将Python标准库日志重定向到Loguru[5,8](@ref)"""
        class InterceptHandler(logging.Handler):
            def emit(self, record):
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno
                logger.opt(depth=6, exception=record.exc_info).log(
                    level, record.getMessage()
                )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
            logging.getLogger(name).handlers = [InterceptHandler()]

    @property
    def _console_format(self):
        """控制台日志格式（含请求追踪ID）[7](@ref)"""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "req_id:{extra[request_id]} - <level>{message}</level>"
        )

    @property
    def _file_format(self):
        """文件日志格式"""
        return (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
            "{level: <8} | "
            "{module}.{function}:{line} | "
            "req_id:{extra[request_id]} - {message}"
        )

    def _filter_uvicorn(self, record):
        """过滤Uvicorn原生日志[5](@ref)"""
        return "uvicorn" not in record["message"]

    def bind_request_id(self, request: Request):
        """绑定请求追踪ID[7](@ref)"""
        req_id = request.headers.get("X-Request-ID") or self._generate_id()
        self.request_id.set(req_id)
        logger.configure(extra={"request_id": req_id})

    @staticmethod
    def _generate_id() -> str:
        """生成12位请求ID"""
        import shortuuid
        return shortuuid.ShortUUID().random(length=12)

# 初始化并导出实例
log_manager = UnifiedLogger()
log = logger