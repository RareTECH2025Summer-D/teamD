#pythonのイメージを使用
FROM python:3.12-slim
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
COPY . .
#Gunicorn が使うポートを開放（ローカル用）EXPOSE は「このポート使うよ」と他のコンテナに教えるだけで、実際の公開は ports で決まるから必須ではない
EXPOSE 8000
#起動するコマンドを指定　Gunicorn（コンテナ内のアプリ）がどのアドレス・ポートで待ち受けるか決める　gunicornのポートとコンテナの８０００ポートを繋げる
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]