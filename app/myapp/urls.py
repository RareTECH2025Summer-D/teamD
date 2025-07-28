from django.urls import path
from .views import ChannelListView
from . import views
from myapp.views import health_check


urlpatterns = [
    path('', ChannelListView.as_view(), name='channel_list'), 
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('health/', health_check, name='health_check')
]
