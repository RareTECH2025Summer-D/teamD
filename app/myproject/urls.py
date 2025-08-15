from django.contrib import admin
from django.urls import path, include
from .views_health import health

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')), 
    path('health', health),
]

