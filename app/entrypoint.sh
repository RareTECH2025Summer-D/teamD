#!/bin/sh

# DB起動待ち
echo " Waiting for MySQL..."
for i in $(seq 1 30); do
  nc -z "$MYSQL_HOST" "3306" && echo " MySQL is up!" && break
  echo " Waiting... ($i)"
  sleep 1
done

# マイグレーション
echo " Running migrations..."
python manage.py migrate

# 静的ファイル収集
echo " Collecting static files..."
python manage.py collectstatic --noinput

# アプリ起動
echo " Starting Gunicorn..."
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
