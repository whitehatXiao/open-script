# 示例脚本 plugins/demo_plugin01.py
# 要求执行插件必须要有统一的 main 函数入口
def main():
    print("执行插件逻辑，测试 01010011")
    return {"status": "success"}