from django.views.generic import ListView, DetailView,CreateView,DeleteView,UpdateView,TemplateView,View
from django.contrib.auth.views import LoginView,LogoutView
from formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect, render
from .models import Channel
from .forms import ChannelForm
from django.http import HttpResponse

"""
# ヘルスチェック
def health_check(request):
    return HttpResponse("OK", status=200)


#ユーザー登録
def signup_view(request):
    return render(request, 'registration/signup.html')

#ログイン
def login_view(request):
    return render(request, 'registration/login.html')



# チャンネル一覧 + チャンネル作成
class ChannelListView(ListView):
    model = Channel
    template_name = 'sample.html'
    context_object_name = 'channels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChannelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ChannelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('channel_list')
"""
# サインアップ
class UserSignup(CreateView):
    pass










# ログイン
class Login(LoginView):
    pass  











# ログアウト
class Logout(LogoutView):
    pass  









# 学ぶ・教える選択
class RoleSelect(TemplateView):
    def get():
          
        pass
    
    def post():
        pass  










# ホーム画面
class UserHome(TemplateView):
    def get():
          
        pass
    
    def post():
        pass  









# 初回スキル登録（学ぶ・教える共通）
class ProfileCreate():
    def get():
          
        pass
    
    def post():
        pass  










# スキル作成
class SkillCreate():
    def get():
          
        pass
    
    def post():
        pass  










# プロフィール作成(学ぶ・教える共通)
class ProfileCreate():
    def get():
          
        pass
    
    def post():
        pass










# プロフィール編集
class ProfileUpdate():
    def get():
          
        pass
    
    def post():
        pass










# 先生・生徒検索(学ぶ・教える共通)
class SearchUsers():
    def get():
          
        pass
    
    def post():
        pass










# ユーザー詳細画面(学ぶ・教える共通)
class UserDitail():
    def get():
          
        pass
    
    def post():
        pass










# リクエスト送信(学ぶ・教える共通)
class SendRequest():
    def get():
          
        pass
    
    def post():
        pass










# リクエスト一覧(学ぶ・教える共通)
class RequestList():
    def get():
          
        pass
    
    def post():
        pass










# 承認・削除送信(学ぶ・教える共通)
class RequestApproval():
    def get():
          
        pass
    
    def post():
        pass










# マッチング成立一覧(学ぶ・教える共通)
class MatchingList():
    def get():
          
        pass
    
    def post():
        pass










# コンタクト
class Contact():
    def get():
          
        pass
    
    def post():
        pass











# 評価
class Review():
    def get():
          
        pass
    
    def post():
        pass










