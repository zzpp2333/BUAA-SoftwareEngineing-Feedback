from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import UserProfile
from course.models import CourseUsers
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.urls import reverse

# Create your views here.


def register(request):
    if request.method == 'POST':
        permission = 1
        username = request.POST['username']
        password = request.POST['password']
        no = request.POST['no']
        email = request.POST['email']

        if len(UserProfile.objects.filter(no=no)) > 0:
            return HttpResponse(json.dumps({'permission': 0, 'error': '学号/工号已注册'}), content_type='application/json')

        if len(User.objects.filter(username=username)) > 0:
            return HttpResponse(json.dumps({'permission': 0, 'error': '用户名已存在'}), content_type='application/json')

        if len(User.objects.filter(email=email)) > 0:
            return HttpResponse(json.dumps({'permission': 0, 'error': '邮箱已注册'}), content_type='application/json')


        user = User.objects.create_user(username=username, password=password, email=email)

        if len(no) == 5:
            permission = 2
        else:
            permission = 1

        # if username == 'student':
        #     permission = 1
        # elif username == 'teacher2':
        #     permission = 2
        # elif username == 'assistant':
        #     permission = 3
        # elif username == 'eduadmin':
        #     permission = 4
        user_profile = UserProfile(user=user, permission=permission, no=no)
        user_profile.save()

        if permission != 4:
            course_user = CourseUsers(user=user)
            course_user.save()

        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session.set_expiry(0)
            request.session['id'] = user.id

            if permission == 1:
                url = '/stu_resource/'
            elif permission == 2:
                url = '/teacher_resource/'
            elif permission == 4:
                url = '/edu_admin_resource/'
            else:
                url = '/'

            return HttpResponse(json.dumps({'url': url, 'permission': permission}), content_type='application/json')

    return render(request, 'studentsystem/register.html')


def login(request):
    # print(request.user.is_authenticated())
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(username)
        # print(password)

        if len(User.objects.filter(username=username)) == 0:
            return HttpResponse(json.dumps({'permission': 0, 'error': '用户名不存在'}), content_type='application/json')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            request.session.set_expiry(0)
            request.session['id'] = user.id
            print(request.session['id'])
            return HttpResponse(json.dumps({'permission': user.profile.permission}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'permission': 0, 'error': '密码不正确'}), content_type='application/json')
    return render(request, 'studentsystem/login.html')


def _logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def test(request):
    print(request.session['id']+1)
    return render(request, 'users/test.html', {'msg': User.objects.last().course_s_link.test})


def create_edu_admin(request):
    user = User.objects.create_user(username='admin', password='admin')

    user_profile = UserProfile(user=user, permission=4)
    user_profile.save()
    return HttpResponse(json.dumps({'msg': 'success'}))


def getUserInfos(request):
    if request.method == 'GET':
        user_id = request.user.id
        user = User.objects.get(id=user_id)

        return HttpResponse(json.dumps({
            'username': user.username,
            'userno': user.profile.no,
            'permission': user.profile.permission,
            'email': user.email
        }), content_type='application/json')