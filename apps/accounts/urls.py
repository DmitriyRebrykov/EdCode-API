from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.courses.views import CategoryViewSet, CourseViewSet, LessonViewSet

router = routers.DefaultRouter()

app_name = 'accounts'
urlpatterns = [
    path('', include(router.urls))
]