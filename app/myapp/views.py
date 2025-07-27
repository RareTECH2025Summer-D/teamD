from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import Channel
from .forms import ChannelForm
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", status=200)

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

