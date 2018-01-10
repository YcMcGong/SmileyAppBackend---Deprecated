"""SmileyAppBackend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('helloworld/', include('SmileyWorld.urls')),
    path('admin/', admin.site.urls),
]
