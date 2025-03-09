# 安装依赖
# pip install requirements.txt 

# 执行
# uvicorn main:app --reload 
# uvicorn main:app --reload --log-level debug


# Unit Test
curl.exe -X POST "http://localhost:8000/scripts/execute/demo_plugin1"
curl.exe -X POST "http://localhost:8000/scripts/execute/demo_plugin2"
curl.exe -X POST "http://localhost:8000/scripts/execute/demo_plugin3"

curl.exe -X POST -F "file=@demo_plugin.py" http://localhost:8000/scripts/upload
curl.exe -X POST -F "file=@demo_plugin1.py" http://localhost:8000/scripts/upload
curl.exe -X POST -F "file=@demo_plugin2.py" http://localhost:8000/scripts/upload
curl.exe -X POST -F "file=@demo_plugin3.py" http://localhost:8000/scripts/upload
