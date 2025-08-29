from django.contrib import admin
from .models import Users, UserProfile, Skills, UserSkills, Matchings
from .models import Users, UserProfile, Skills, UserSkills
from django.contrib.sessions.models import Session

admin.site.register(Users)
admin.site.register(UserProfile)
admin.site.register(Skills)
admin.site.register(UserSkills)
admin.site.register(Matchings)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date', 'get_decoded_data']

    def get_decoded_data(self, obj):
        return obj.get_decoded()
    get_decoded_data.short_description = 'Session Data'
