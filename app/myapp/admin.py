from .models import Users, UserProfile, Skills, UserSkills, Channel

from django.contrib import admin
from .models import Users, UserProfile, Skills, UserSkills, Channel

admin.site.register(Users)
admin.site.register(UserProfile)
admin.site.register(Skills)
admin.site.register(UserSkills)
admin.site.register(Channel)

