#pythonのイメージを使用
FROM python:3.12-slim
#必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config\
    netcat-openbsd
#カレントディレクトリを指定
WORKDIR /app
#pythonパッケージをまとめてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#pythonディレクトリの内容をコンテナにコピー
COPY . .
# 実行できるようにする
RUN chmod +x entrypoint.sh
#使うポートを開放（ローカル用）EXPOSE は「このポート使うよ」と他のコンテナに教えるだけで、実際の公開は ports で決まるから必須ではない
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]  