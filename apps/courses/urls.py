from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from apps.courses.views import CategoryViewSet, CourseViewSet, LessonViewSet


app_name = 'courses'
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls))
]