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

    
    


# 学ぶ教える選択画面（作成中）
class RoleForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['just_before_status']
    
    
    # 選択肢定義のリスト
    ROLE_CHOICES = [
        (True, '教える'),   # タプル型(値,表示テキスト)
        (False, '学ぶ'), 
    ]
    

# スキル選択画面（作成中）
class SkillSelectForm(forms.ModelForm):

    # skillsよりスキル一覧を取得
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        skill_choices = [(skill.name, skill.name) for skill in Skills.objects.all()] # スキル名をタプル型にし、List形式で格納

        self.fields['selected_skills'] = forms.MultipleChoiceField(
            choices=skill_choices
            , widget=forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'skill-checkbox'
                    , 'id': {{ skill.id }}
                    , 'name': 'skill_name[]'
                }
            )
            , required=False
        )


# スキル作成
class SkillCreationForm(forms.ModelForm):
    skill_name = forms.CharField(max_length=100)


# プロフィール作成・編集
class ProfileForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50)
    contact_info = forms.EmailField
    self_introduction = forms.CharField

