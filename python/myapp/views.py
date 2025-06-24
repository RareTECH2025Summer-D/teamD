from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import Channel, Message
from .forms import ChannelForm, MessageForm

# チャンネル一覧 + チャンネル作成
class ChannelListView(ListView):
    model = Channel
    template_name = 'channels.html'
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

# チャンネル詳細 + メッセージ投稿
class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'channel_detail.html'
    context_object_name = 'channel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.channel = self.object
            msg.save()
        return redirect('channel_detail', pk=self.object.pk)

