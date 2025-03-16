# types/constants.py
from pathlib import Path
from typing import Final

class ConstantsMeta(type):
    """元类实现常量不可修改特性"""
    def __setattr__(cls, name, value):
        if name in cls.__dict__:
            raise AttributeError(f"常量 {name} 禁止二次赋值")
        super().__setattr__(name, value)

class Constants(metaclass=ConstantsMeta):
    """全局常量类（强制不可修改）"""

    # 基础路径
    PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.resolve()
    PLUGIN_DIR: Final[Path] = PROJECT_ROOT / "resources/plugins"
    LOG_DIR: Final[Path] = PROJECT_ROOT / "logs"
    SCRIPTS_DIR: Final[Path] = PROJECT_ROOT / "resources/scripts"
    RESOURCE_DIR: Final[Path] = PROJECT_ROOT / "resources"
    RESULT_DIR: Final[Path] = PROJECT_ROOT / "resources/results"
    DEVOPS_DIR: Final[Path] = PROJECT_ROOT / "devops"

    # 业务常量
    MAX_CONCURRENT_TASKS: Final[int] = 10
    SUPPORTED_EXTENSIONS: Final[tuple] = (".py", ".json")


    # 动态资源加载
    @classmethod
    def get_resource(cls, relative_path: str) -> Path:
        """安全获取资源路径"""
        return (cls.PROJECT_ROOT / relative_path).resolve()