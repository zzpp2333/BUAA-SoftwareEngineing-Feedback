from django.urls import path, include
from . import views

urlpatterns = [
    path('test/', views.test),
    path('addCourse/', views.addCourse),
    path('test2/', views.test2),
    path('getCourses/', views.getCourses),
    path('applyAssistant/', views.applyAssistant),
    path('relateAssistant/', views.relateAssistant),
    path('getss/', views.getss),
    path('relatess/', views.relatess),
    path('getAssistApplications/', views.getAssistApplications),
    path('getCourseUsers/', views.getCourseUsers),
    path('checkCourse/', views.checkCourse),
]