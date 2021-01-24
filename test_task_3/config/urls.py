"""
config URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from test_task.views import MainPageView


urlpatterns = [
    path('', MainPageView.as_view()),
    path('admin/', admin.site.urls),
]
