from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from .models import Channel
from .forms import ChannelForm
from django.http import HttpResponse


# ヘルスチェック
def health_check(request):
    return HttpResponse("OK", status=200)


#ユーザー登録
def signup_view(request):
    return render(request, 'registration/signup.html')

#ログイン
def login_view(request):
    return render(request, 'registration/login.html')

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

