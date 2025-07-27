from django.urls import path
from .views import ChannelListView , health_check

urlpatterns = [
    path('', ChannelListView.as_view(), name='channel_list'), 
    path("health/", health_check),
]
