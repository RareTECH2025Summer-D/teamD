from django.urls import path
from .views import ChannelListView
from . import views
from myapp.views import health_check


urlpatterns = [
    path('', ChannelListView.as_view(), name='channel_list'), 
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('user/setup/skill', views.skill_setup_view, name='setup_skill'),
    path('user/create/skill', views.skill_create_view, name='create_skill'),
    path('user/setup/profile', views.profile_create_view, name='setup_profile'),
    path('health/', health_check, name='health_check')
]
