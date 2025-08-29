# teamD - 開発用 Django アプリ

## 📦 使用技術

- Python 3.12  
- Django  
- Docker / Docker Compose  
- MySQL（開発用 DB）

---

## 🚀 開発環境の立ち上げ

### 1. `.env` ファイルの作成（`.env.example` をコピー）

```bash
cp .env.example .env
```

2. ビルド & 起動
```bash
docker compose up --build
```
3. マイグレーション（初回のみ）
```bash
docker compose exec app python manage.py migrate
```
4. 管理ユーザーの作成（初回のみ）
```bash
docker compose exec app python manage.py createsuperuser
```
→ ユーザー名・メール・パスワードを入力

🧪 動作確認
URL	説明
```bash
http://localhost:8000/	ログイン画面
http://localhost:8000/admin/	Django 管理画面（ログイン必要）
```

