# 1. 使用 Python 3.14 的 Linux 環境
FROM python:3.14-slim

# 2. 設定容器內的工作資料夾
WORKDIR /app

# 3. 複製 Python 套件清單
COPY requirements.txt .

# 4. 安裝所需套件
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製專案程式碼
COPY . .

# 6. 宣告 API 使用的連接埠
EXPOSE 8000

# 7. 啟動 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 8. 安裝 Linux 的 Ping 工具 iputils-ping
RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping \
    && rm -rf /var/lib/apt/lists/*