# MyApp

練習用の **Django + MySQL + Nginx** の Docker構成プロジェクトです。

---

## 🚀 Requirements

- Docker
- Docker Compose

---

## ⚙️ .env の作成

まず、プロジェクトルートに `.env` を作成してください。

```env
# .env
MYSQL_ROOT_PASSWORD=example
MYSQL_DATABASE=mydb
MYSQL_USER=root
MYSQL_PASSWORD=example

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
.env.example を参考にしてもOKです。

🔧 初期セットアップ
以下のコマンドで初期化してください。

# イメージのビルドとコンテナ起動
docker-compose up --build

# 初回のみマイグレーションを実行
docker-compose exec app python manage.py migrate

# 必要に応じてスーパーユーザー作成
docker-compose exec app python manage.py createsuperuser

✅ 動作確認
URL	説明
http://localhost/	トップページ (Nginxが返す静的HTML)
http://localhost/channels/	チャンネル一覧 (Django)
http://localhost/admin/	管理画面 (Django, 任意)

📦 ディレクトリ構成

.
├── docker-compose.yml
├── env.example
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/
│   │   └── app.conf
│   └── html/
│       └── index.html
└── python/
    ├── Dockerfile
    ├── requirements.txt
    ├── manage.py
    ├── myapp/
    │   ├── ...
    └── myproject/
        ├── settings.py
        ├── urls.py
        └── wsgi.py
