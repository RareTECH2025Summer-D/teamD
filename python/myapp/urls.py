from django.urls import path
from .views import ChannelListView, ChannelDetailView

urlpatterns = [
    path('', ChannelListView.as_view(), name='channel_list'),  # ルート
    path('channels/', ChannelListView.as_view(), name='channel_list'),
    path('channels/<int:pk>/', ChannelDetailView.as_view(), name='channel_detail'),
]
