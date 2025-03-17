


## 项目背景
公司当前希望借助工具去大幅度缩减员工的重复性工作，例如excel表格处理等
计划开发的应用：开放插件平台系统

## 需求分析与原型验证
需求说明： 公司平台人员（财务人员）经常需要统计各办事处（公司各分支）的财务、销售数据，经常会涉及到多表格的整合修改，如果纯通过手工的方式处理合并excel等表格，效率太低。 所以我作为一名软件工程，希望写一个“提供python脚本上传、存储、调用、执行的框架平台” 系统。

1、对于平台人员，可以将要处理的表格(多个)上传到网页平台中，选择需要之前上传过的脚本，系统内部进行执行，并输出结果，系统内部的过程，普通用户无需关注；

2、对于脚本提供人员，提供一个接口，让公司各个分支的，有技术背景的人员，能够上传脚本。 总结下来，这个系统需要考虑用户界面、后端架构、安全隔离、权限控制、任务管理、文件存储、脚本规范、错误处理、日志记录、性能扩展等多个方面。 需要分阶段开发，先实现核心功能，再逐步完善安全性和用户体验。

同时，和用户沟通确认需求的优先级，确保首先满足最关键的需求，比如安全执行和基本的上传、执行功能。

技术栈（原型版）
    前端： 先忽略，用curl验证接口
    后端：
        web框架： fastapi
        动态加载器： importlib
        数据库： sqlite
        日志框架: loguru
        授权鉴权： jwt+切面编程
    执行：
        采用容器部署和执行
        open-script容器：负责业务逻辑处理和目录创建
        FileBrowser容器：负责文件读写和权限验证
    数据一致性：两容器共享同一存储卷，避免数据冗余
    存储： 暂时本地存储，存储表格和脚本
    任务队列: 暂时使用同步方案


## 系统设计与规划

原型版本的业务流程
![img_4.png](img_4.png)
系统用例图
![img_5.png](img_5.png)

# Dockerfile 构建运行
docker build -t open-script:v0.1 .
docker run -d --name MyOpenScript -p 9999:8000 open-script:v0.1
docker exec -it <容器名称或ID> /bin/bash

# 安装依赖
# pip install requirements.txt 

# 执行
# uvicorn main:app --reload 
# uvicorn main:app --reload --log-level debug

# 接口测试
本地测试
## 上传文件
curl.exe -X POST -F "file=@demo01.py" http://localhost:8000/scripts/upload
curl.exe -X POST -F "file=@demo02.py" http://localhost:8000/scripts/upload
## 执行脚本
curl.exe -X POST "http://localhost:8000/scripts/execute/demo01"
curl.exe -X POST "http://localhost:8000/scripts/execute/demo02"
## 用户注册
curl.exe  -X POST -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"admin\"}" http://127.0.0.1:8000/users/register 
## 登录获取令牌
curl.exe -X POST -H "Content-Type: application/json" -d "{\"username\": \"admin\", \"password\": \"admin\"}" http://localhost:8000/users/login
resp： 
{"code":200,"data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZTcyZjg3Zi05Nzg3LTRlMjQtOGNiZS02YTVhNmEwMGRjZGUiLCJleHAiOjE3NDIxMTk1NTh9.1nt-EZALoDl93PYtWkbnmMfsV2TM4__XHRfuLZWWRHw","token_type":"bearer"},"message":"登录成功"}
## 使用令牌访问受保护接口
/user/me
curl.exe -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZTcyZjg3Zi05Nzg3LTRlMjQtOGNiZS02YTVhNmEwMGRjZGUiLCJleHAiOjE3NDIxMjUzOTh9.hezo7wgWWwdyfloO36DMsuP9FpxSs4di7e89cDQLw-Y" http://localhost:8000/users/me
/upload
curl.exe -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZTcyZjg3Zi05Nzg3LTRlMjQtOGNiZS02YTVhNmEwMGRjZGUiLCJleHAiOjE3NDIxMjUzOTh9.hezo7wgWWwdyfloO36DMsuP9FpxSs4di7e89cDQLw-Y" -X POST -F "file=@demo01.py" http://localhost:8000/scripts/upload
/execute
curl.exe -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZTcyZjg3Zi05Nzg3LTRlMjQtOGNiZS02YTVhNmEwMGRjZGUiLCJleHAiOjE3NDIxMjUzOTh9.hezo7wgWWwdyfloO36DMsuP9FpxSs4di7e89cDQLw-Y" -X POST "http://localhost:8000/scripts/execute/demo01"


# 脚本开发标准
1、 用 main 函数作为入口，执行脚本
2、 脚本执行时，需要返回一个字典，包含以下字段： TODO 待完善

## 优化记录
