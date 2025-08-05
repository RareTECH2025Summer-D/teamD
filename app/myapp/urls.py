from django.urls import path
from .views import *
#ChannelListView
from . import views
from myapp.views import health_check


urlpatterns = [
    # path('', ChannelListView.as_view(), name='channel_list'), 
    # path('signup/', views.signup_view, name='signup'),
    # path('login/', views.login_view, name='login'),
    # path('health/', health_check, name='health_check')
    path('signup/',UserSignup.as_view(template_name='signup.html'),name='signup'),
    path('login/',Login.as_view(template_name='login.html'),name='login'),
    path('logout/',Logout.as_view(template_name='settings.html'),name='logout'),
    path('select/role/',RoleSelect.as_view(template_name=''),name='select_role'),
    path('user/home/',UserHome.as_view(template_name='home.html'),name='user_home'),
    path('user/setup/skill/',ProfileCreate.as_view(template_name='skill_registration.html'),name='user_setup_skill'),
    path('user/create/skill',SkillCreate.as_view(template_name='未定'),name='user_create_skill'),
    path('user/setup/profile/',ProfileCreate.as_view(template_name='profile_create.html'),name='user_setup_profile'),
    path('user/update/profile/',ProfileUpdate.as_view(template_name='profile_edit.html'),name='user_update_profile'),
    path('search/',SearchUsers.as_view(template_name='search.html'),name='search'),
    path('user/detail',UserDitail.as_view(template_name='未定'),name='user_detail'), # HTMLファイル名の確認
    path('request/send',SendRequest.as_view(),name='request_send'),
    path('request/list/',RequestList.as_view(template_name='handshake.html'),name='request_list'),
    path('request/approval/',RequestApproval.as_view(template_name=''),name='request_approval'),
    path('matching/list/',MatchingList.as_view(template_name='handshake.html'),name='matching_list'),
    path('contact/user/',Contact.as_view(template_name='未定'),name='contact_user'),
    path('reviewt/user/',Review.as_view(template_name='未定'),name='reviewt_user'),
]
