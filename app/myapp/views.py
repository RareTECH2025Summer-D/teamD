from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
from .models import Channel
from .forms import ChannelForm


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

