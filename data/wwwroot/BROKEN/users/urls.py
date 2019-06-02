from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views._logout, name='_logout'),
    path('test/', views.test),
    path('getUserInfos/', views.getUserInfos)
    # path('create_edu_admin/', views.create_edu_admin)
]