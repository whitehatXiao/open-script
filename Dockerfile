# 基于官方Python镜像构建（集成脚本执行环境）
FROM python:3.11-slim

# 设置容器环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    SCRIPTS_DIR=/open-script/resources/scripts \
    PLUGINS_DIR=/open-script/resources/plugins \
    RESULTS_DIR=/open-script/resources/results \
    APP_HOME=/open-script

# 创建目录结构
RUN mkdir -p $APP_HOME $SCRIPTS_DIR $PLUGINS_DIR $RESULTS_DIR /var/log/app \
    && chmod 777 $SCRIPTS_DIR

# 安装编译依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR $APP_HOME

# 先复制依赖文件以利用Docker缓存
COPY requirements.txt .

# 安装Python依赖（包含FastAPI核心组件）
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install fastapi uvicorn python-multipart

# 复制应用代码（将构建上下文（Dockerfile所在目录）的所有文件/子目录复制到容器内的$APP_HOME）
COPY . .

# 配置容器入口
USER root
# 端口声明
EXPOSE 8000

# 调整后（直接运行main.py）
CMD ["python", "main.py"]