from django.urls import path, include
from . import views

urlpatterns = [
    path('createtopic/', views.createtopic),
    path('gettopics/', views.gettopics),
    path('getreplies/', views.getreplies),
    path('reply/', views.reply),
    path('getSimilarTopics/', views.getSimilarTopics),
]