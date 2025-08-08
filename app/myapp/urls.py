from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('signup/',UserSignup.as_view(template_name='registration/signup.html'),name='signup'),
    path('login/',Login.as_view(template_name='registration/login.html'),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),                                 # DjangoのLogoutViewで完結
    path('select/role/',RoleSelect.as_view(template_name='settings.html'),name='select_role'),
    path('user/home/',UserHome.as_view(template_name='home.html'),name='user_home'),
    # path('user/setup/skill/',ProfileCreate.as_view(),name='user_setup_skill'),          # View継承のためtemplate_nameなし
    # path('user/create/skill',SkillCreate.as_view(),name='user_create_skill'),           # View継承のためtemplate_nameなし
    path('user/setup/profile/',ProfileCreate.as_view(),name='user_setup_profile'),      # View継承のためtemplate_nameなし
    path('setting/',Setting.as_view(template_name='setting.html'),name='setting'),
    path('user/update/profile/',ProfileUpdate.as_view(template_name='profile_edit.html'),name='user_update_profile'),
    path('search/',SearchUsers.as_view(template_name='search.html'),name='search'),
    path('user/detail',UserDitail.as_view(template_name='user_profile.html'),name='user_detail'),
    path('request/send',SendRequest.as_view(),name='request_send'),
    path('request/list/',RequestList.as_view(template_name='handshake.html'),name='request_list'),
    path('request/approval/',RequestApproval.as_view(),name='request_approval'),
    path('matching/list/',MatchingList.as_view(template_name='handshake.html'),name='matching_list'),
    path('contact/user/',Contact.as_view(),name='contact_user'),                        # POPのみ
    path('reviewt/user/',Review.as_view(template_name='matching.html'),name='reviewt_user'),
    path('user/setup/skill', views.skill_setup_view, name='setup_skill'),
    path('user/create/skill', views.skill_create_view, name='user_create_skill'),
    path('user/setup/profile', views.profile_create_view, name='user_setup_profile'),
]