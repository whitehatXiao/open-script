# logger.py
import sys
import logging
from pathlib import Path
from loguru import logger
from type.constants import Constants

class LightLogger:
    """轻量级日志模块（保留切割与标准库接管）"""

    def __init__(self):
        self.log_dir = Constants.LOG_DIR
        self._init_config()

    def _init_config(self):
        # 单次创建日志目录
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # 移除默认配置
        logger.remove()

        # 控制台输出（简化格式）
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{module}</cyan> - <level>{message}</level>",
            level="INFO",
            enqueue=True  # 异步安全[5](@ref)
        )

        # 文件切割策略（按大小+时间）
        logger.add(
            self.log_dir / "app.log",
            rotation="10 MB",  # 按大小切割[5](@ref)
            retention="7 days",  # 保留周期[2](@ref)
            compression=None,   # 禁用压缩
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module} - {message}",
            level="DEBUG"
        )

        # 接管标准日志库（精简版）
        self._redirect_standard_logging()

    def _redirect_standard_logging(self):
        """接管Python标准日志库[5,7](@ref)"""
        class InterceptHandler(logging.Handler):
            def emit(self, record):
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno
                logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

        logging.basicConfig(handlers=[InterceptHandler()], level=0)

# 初始化即生效
log = logger
LightLogger()