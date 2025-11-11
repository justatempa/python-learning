FROM python:3.11-slim

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone \
    && apt update && apt install weasyprint -y

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8010", "main:app", "--workers", "4"]