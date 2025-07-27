from django.urls import path
from .views import ChannelListView , health_check
from . import views
urlpatterns = [
    path('', ChannelListView.as_view(), name='channel_list'), 
    path("health/", health_check),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login')
]
