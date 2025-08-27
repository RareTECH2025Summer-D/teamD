from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *

# Metaはモデルに存在するフィールドを、入力フォームにそのまま利用できる（12行目）
# モデルにないものに関しては、Metaの外で定義する
# widgetでCSSのクラスやidなどを設定できる

# ログイン画面（作成中）
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # username フィールドのウィジェットをカスタマイズ
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'registration-form',
            'placeholder': 'Email',
            'required': True,
        })
        
        # password フィールドのウィジェットをカスタマイズ
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'registration-form',
            'placeholder': 'パスワード',
            'required': True,
        })

        self.error_messages['invalid_login'] = 'メールアドレスまたはパスワードが間違っています。'

        
# サインアップ画面
class SignupForm(forms.ModelForm):
    
    password = forms.CharField(label=''
        ,widget=forms.PasswordInput(
            attrs={
                'class': 'registration-form'    # CSSのクラス
                , 'name': 'password1'           # name
                , 'placeholder': 'パスワード'    # プレイスホルダー
                , 'required':True               # 必須項目
            }
        )
    )
    confirmation_password = forms.CharField(label=''
        ,widget=forms.PasswordInput(
            attrs={
                'class': 'registration-form'        # CSSのクラス
                , 'name': 'password2'               # name
                , 'placeholder': 'パスワード確認用'  # プレイスホルダー
                , 'required':True                   # 必須項目
            }
        )
    )
    
    # modelと紐づけ
    class Meta:
        model = Users
        fields = ['email'] # passwordはform.save()で保存されるリスクを回避のためにフィールド設定しない
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'registration-form'
                    , 'name': 'email'
                    , 'placeholder': 'Email'
                    , 'required':True
                }
            )
        }
        # ラベルなし設定
        labels = {
            'email': ''
        }

    # 検証メソッド
    def clean(self):
        cleaned_data = super().clean()          # フォームのデータをすべて取得
        password = cleaned_data.get("password") # 取得したフォームデータからpassword取得
        confirmation_password = cleaned_data.get("confirmation_password")

        # 入力の確認とパスワード一致の確認
        if password and confirmation_password and password != confirmation_password:
            raise forms.ValidationError('パスワードを確認')
        
        return cleaned_data


# 学ぶ教える選択画面
class RoleForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['just_before_status']
    
    
    # 選択肢定義のリスト
    ROLE_CHOICES = [
        (True, '教える'),   # タプル型(値,表示テキスト)
        (False, '学ぶ'), 
    ]
    

# スキル選択画面
# モデルの作成更新は行わないため、forms.Formを利用
class SkillSelectForm(forms.Form):

    # skillsよりスキル一覧を取得
    # filter(skill_count__=10)→count が指定された値 (10) 以上 (greater than or equal to) である」という条件を指定するフィールドルックアップ
    skills = forms.ModelMultipleChoiceField(
        queryset = Skills.objects.filter(skill_count__gte=10),
        widget = forms.CheckboxSelectMultiple(
            attrs = {'class':'skill-checkbox'}
        ),
        required=False,
    )

    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# スキル作成
class SkillCreationForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill_name']
        widgets = {
            'skill_name':forms.TextInput(
                attrs={
                    'class':'skill-form'
                    , 'name':'skill_name'
                    , 'required': True
                }
            )
        }

        labels = {
            'skill_name':''
        }
    # スキル名がSkillsに存在するかチェック
    def clean_skill_name(self):
        skill_name = self.cleaned_data.get("skill_name")
        if Skills.objects.filter(skill_name=skill_name).exists():
            raise forms.ValidationError("このスキルはすで登録されています")
        else:
            return skill_name



# プロフィール作成・編集
class ProfileForm(forms.ModelForm):
    # forms.py
    class Meta:
        model = UserProfile
        fields = ["nickname", "self_introduction", "contact_info"]
        widgets = {
                "nickname": forms.TextInput(
                    attrs={
                        "class": "profile-form",
                        "id": "user_name",
                        "type": "text",   # 明示
                        "name": "user_name",  # 明示（通常は自動でnicknameになる）
                    }
                ),
                "contact_info": forms.TextInput(
                    attrs={
                        "class": "profile-form",
                        "id": "contact_info",
                        "type": "text",
                        "name": "contact_info",
                    }
                ),
                "self_introduction": forms.Textarea(
                    attrs={
                        "class": "introduction-form",
                        "id": "self_introduction",
                        "maxlength": "255",
                    }
                ),
            }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            if not self.data:
                self.fields["contact_info"].initial = self.instance.contact_info or user.email