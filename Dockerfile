FROM python:3.10-slim

# Cài thư viện cần thiết để Chrome headless hoạt động
RUN apt-get update && apt-get install -y \
    wget gnupg unzip xvfb libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 libxss1 libappindicator3-1 libasound2 curl \
    && rm -rf /var/lib/apt/lists/*

# Cài Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install ./google-chrome-stable_current_amd64.deb -y && \
    rm google-chrome-stable_current_amd64.deb

# Copy mã nguồn
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

# Chạy với xvfb-run để xử lý headless Chrome
CMD ["xvfb-run", "python", "main.py"]
