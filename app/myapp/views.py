from django.views.generic import ListView, DetailView,CreateView,UpdateView,TemplateView,View
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import redirect, render
# from django.http import HttpResponse

# サインアップ
class UserSignup(CreateView):
    model = Users
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # フォームが有効な際に実行
        user = form.save(commit=False)                      # 入力フォームの情報を取得
        user.set_password(form.cleaned_data["password"])    # passwordをハッシュ化
        user.save()
        return super().form_valid(form)
        

# ログイン
class Login(LoginView):
    model = Users
    loginform = SignupForm
    success_url = reverse_lazy('user_home')






# スキル登録画面
def skill_setup_view(request):
    # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
    role = request.GET.get("role", "student")

    if role == "student":
        page_title = "学びたいスキルを<br>選択してください！"
    elif role == "teacher":
        page_title = "教えたいスキルを<br>選択してください！"
    
    return render(request, 'app/skill_registration.html', {
        "role": role,
        "page_title": page_title,
    })

# スキル作成画面
def skill_create_view(request):
    role = request.GET.get("role", "student")

    if role == "student":
        page_title = "学びたいスキルを<br>作りましょう！"
    elif role == "teacher":
        page_title = "教えたいスキルを<br>作りましょう！"

    return render(request, 'app/skill_create.html', {
        "role": role,
        "page_title": page_title
    })

# プロフィール作成画面
def profile_create_view(request):
    # 開発用にURLパラメータでroleを取得。なければデフォルトをstudentにする
    role = request.GET.get("role", "student")
    
    return render(request, 'app/profile_create.html', {
        "role": role,
    })












# ホーム画面
class UserHome(TemplateView):
    def get():

        pass

    def post():
        pass  









# 学ぶ・教える選択
class RoleSelect(TemplateView):
    def get():

        pass

    def post():
        pass  











# 初回スキル登録（学ぶ・教える共通）
# View継承時はtemplate_nameでHTMLファイル指定できないので、render()関数でHTMLファイルの指定をする
class ProfileCreate(View):
    def get():

        # return render(request, 'skill_registration.html', context)
        pass

    def post():
        pass  










# スキル作成
# HTMLファイル確認
class SkillCreate(View):
    def get():

        # return render(request, '.html', context)
        pass

    def post():
        pass  










# プロフィール作成(学ぶ・教える共通)
class ProfileCreate(View):
    def get():

        # return render(request, 'profile_create.html', context)
        pass

    def post():
        pass













#設定画面
class Setting(TemplateView):
    pass

     











# プロフィール編集
class ProfileUpdate(UpdateView):
    def get():

        pass

    def post():
        pass










# 先生・生徒検索(学ぶ・教える共通)
class SearchUsers(ListView):
    def get():

        pass

    def post():
        pass










# ユーザー詳細画面(学ぶ・教える共通)
class UserDitail(DetailView):
    def get():

        pass

    def post():
        pass










# リクエスト送信(学ぶ・教える共通)
class SendRequest(TemplateView):
    def get():

        pass

    def post():
        pass










# リクエスト一覧(学ぶ・教える共通)
class RequestList(ListView):
    def get():

        pass

    def post():
        pass










# 承認・削除送信(学ぶ・教える共通)
class RequestApproval(TemplateView):
    def get():

        pass

    def post():
        pass










# マッチング成立一覧(学ぶ・教える共通)
class MatchingList(ListView):
    def get():

        pass

    def post():
        pass










# コンタクト
class Contact(TemplateView):
    def get():

        pass

    def post():
        pass











# 評価
class Review(CreateView):
    def get():

        pass

    def post():
        pass



