# 安装依赖
# pip install requirements.txt 

# 执行
# uvicorn main:app --reload 
# uvicorn main:app --reload --log-level debug


# 单元测试用例
## 接口测试
### 本地测试
curl.exe -X POST "http://localhost:9999/scripts/execute/demo_plugin01"
curl.exe -X POST "http://localhost:9999/scripts/execute/demo_plugin02"
curl.exe -X POST "http://localhost:9999/scripts/execute/demo_plugin03"

curl.exe -X POST -F "file=@demo_plugin01.py" http://localhost:9999/scripts/upload
curl.exe -X POST -F "file=@demo_plugin02.py" http://localhost:9999/scripts/upload
curl.exe -X POST -F "file=@demo_plugin03.py" http://localhost:9999/scripts/upload
### 服务器测试
curl.exe -X POST "http://116.205.243.195:9999/scripts/execute/demo_plugin01"
curl.exe -X POST "http://116.205.243.195:9999/scripts/execute/demo_plugin02"
curl.exe -X POST "http://116.205.243.195:9999/scripts/execute/demo_plugin03"

curl.exe -X POST -F "file=@demo_plugin01.py" http://116.205.243.195:9999/scripts/upload
curl.exe -X POST -F "file=@demo_plugin02.py" http://116.205.243.195:9999/scripts/upload
curl.exe -X POST -F "file=@demo_plugin03.py" http://116.205.243.195:9999/scripts/upload


# 脚本开发标准
1、 用 main 函数作为入口，执行脚本
2、 脚本执行时，需要返回一个字典，包含以下字段： TODO 待完善

# Dockerfile 构建及运行
docker build -t open-script:v0.1 .
docker run -d --name MyOpenScript -p 9999:8000 open-script:v0.1
docker exec -it <容器名称或ID> /bin/bash