from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
# Create your models here.

class MyUserManager(BaseUserManager):
    
    # user作成メソッド
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        # メールアドレスを小文字に変換するなど正規化する処理
        email = self.normalize_email(email)
        #インスタンスの作成　self.modelはMYUserManagerが紐づくUserモデルを指す
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # パスワードをハッシュ化して保存
        user.save(using=self._db)  # データベースに保存
        return user
    
    # superuser作成メソッド manage.py createsuperuserで呼び出す
    # userと区別するためにis_staffとis_superuserを追加した状態でcreateuserを呼び出し作成する
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Usersテーブルの定義　AbstractBaseUserを継承しているためpasswordフィールドが自動的に追加される
class Users(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique= True)
    just_before_status = models.BooleanField(blank=True, null=True)  # 初回登録時セッションを保持して登録できる？
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # アカウントが有効かどうか
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = MyUserManager()  # カスタムマネージャーを指定
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#---------------追記-----------------------
    # AbstractBaseUserの場合、権限処理が必要
    # 管理画面で必要となるメソッドを自分で実装 
    def has_perm(self, perm, obj=None):
        # is_superuserがTrueなら、全てのパーミッションを持つとみなす
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        # is_superuserがTrueなら、全てのアプリの管理権限を持つとみなす
        return self.is_superuser

class UserProfile(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=64, blank=True, null=True)
    contact_info = models.CharField(max_length=256, blank=True, null=True)  # 連絡先情報
    is_teacher = models.BooleanField(blank=True, null=True)  # True: 先生, False: 生徒
    self_introduction = models.TextField(blank=True, null=True)
    star_rating_sum = models.IntegerField(default=0)  # 星の合計
    star_rating_count = models.IntegerField(default=0)
    star_rating_average = models.DecimalField(max_digits=1,decimal_places=1)  # 星の平均値
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname # adminの管理画面でデータを文字列として表示させる処理（migrateなど不要）
    
class Skills(models.Model):
    skill_name = models.CharField(max_length = 100)
    serch_tag1 = models.CharField(max_length=100, blank=True, null=True)
    serch_tag2 = models.CharField(max_length=100, blank=True, null=True)
    serch_tag3 = models.CharField(max_length=100, blank=True, null=True)
    skill_count = models.IntegerField(default=0)  # スキルの登録数
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.skill_name

class UserSkills(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(Skills, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(blank=True, null=True)  # True: 先生, False: 生徒
    created_at = models.DateTimeField(auto_now_add=True)  # 登録日時
    updated_at = models.DateTimeField(auto_now=True)
    


class Matchings(models.Model):
    requester_user_id = models.ForeignKey(Users, related_name='requester', on_delete=models.CASCADE)
    requested_user_id = models.ForeignKey(Users, related_name='requested', on_delete=models.CASCADE)
    requester_user_role = models.BooleanField(blank=True, null=True)  # True: 先生, False: 生徒
    requester_status = models.CharField(max_length=20, default='pending')  # リクエストのステータス
    requested_status = models.CharField(max_length=20, default='pending')  # リクエストのステータス
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
class Channel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
