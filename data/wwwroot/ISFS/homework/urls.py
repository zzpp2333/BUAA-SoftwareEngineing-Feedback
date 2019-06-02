"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('getHomework/', views.getHomework),
    path('addHomework/', views.addHomework),
    path('getoneHomework/', views.getoneHomework),
    path('submitHomework/', views.submitHomework),
    path('checkHomework/', views.checkHomework),

    path('Homeworkcontent/', views.Homeworkcontent),
    path('correctHomework/', views.correctHomework),
    path('getstudentGrade/', views.getstudentGrade),
    path('getteacherGrade/', views.getteacherGrade),
    path('studentGrade/', views.studentGrade),
    path('teacherGrade/', views.teacherGrade),
]