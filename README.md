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

# Dockerfile 构建及运行
docker build -t open-script:v0.1 .
docker run -d --name MyOpenScript -p 9999:8000 open-script:v0.1
docker exec -it <容器名称或ID> /bin/bash



# 优化记录
【已修改】1、 魔术属性提取

【已修改】4、 日志系统改进 

【已修改】5、 增加插件元数据接口：通过 GET /plugins 返回已加载插件列表及描

【已修改】6、 请求前缀有多个 ： scripts、 

【已修改】7、 后续后端统一返回标准参数

8、 对上传文件做检查，运行 .py 后缀文件上传

9、 对上传的文件进行依赖分析，没有就先在环境当中去拉取

10、 docker build 时候传入 uvicorn参数 （wh）- mh、sh、ch、wh

11、 fastapi 的线程池调整

12、 fastapi 集成的 swagger api 文档生成

13、 引入统一异常分析器，返回准确答复