import importlib.util
from pathlib import Path
from type.constants import Constants

# 插件加载器
class PluginLoader:
    def __init__(self, plugin_dir=Constants.PLUGIN_DIR):
        self.plugin_dir = plugin_dir
        self.modules = {}

    def load_plugin(self, script_name: str) -> bool:
        """动态加载指定脚本到插件系统"""
        script_path = self.plugin_dir / f"{script_name}.py"
        if not script_path.exists():
            return False

        # 生成唯一模块名（避免冲突）
        module_name = f"plugins.{script_name}"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.modules[script_name] = module
        return True

    def run_plugin(self, script_name: str, func_name: str = "main"):
        """执行插件中的指定函数"""
        if script_name not in self.modules:
            raise ValueError("插件未加载")
        func = getattr(self.modules[script_name], func_name, None)
        if not func or not callable(func):
            raise AttributeError("函数不存在或不可调用")
        return func()