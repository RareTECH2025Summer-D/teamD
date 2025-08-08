#ルートディレクトリでのビルドが必要

#マルチステージ   
FROM python:3.12-slim AS static

#必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config

#カレントディレクトリを指定
WORKDIR /app

#pythonパッケージをまとめてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#pythonディレクトリの内容をコンテナにコピー
COPY app/ .

#collectstatic 実行
ENV ENV_NAME=build_static
RUN python manage.py collectstatic --noinput

#nginx
FROM nginx:alpine

#nginxの設定ファイルをコピー
COPY nginx/conf.d/*.conf /etc/nginx/conf.d

# staticをnginxに
COPY --from=static /app/staticfiles/ /usr/share/nginx/html/static/