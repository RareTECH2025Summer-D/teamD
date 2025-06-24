from django import forms
from .models import Channel, Message

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

