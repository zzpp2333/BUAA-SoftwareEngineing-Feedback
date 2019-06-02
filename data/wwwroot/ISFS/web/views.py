from django.shortcuts import render
from django.contrib.auth.models import User
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.


def hello(request):
    res = {
        'msg': "Hello, Django!"
    }
    return render(request, "test.html", res)


# def login(request):
def test(request):
    res = {
        'permission': 0
    }
    if request.method == 'POST':
        print(request.POST['username'])
        if(request.POST['username'] == 'admin') & (request.POST['password'] == '123456'):
            res = {
                'permission': 2
            }
    return HttpResponseRedirect('/api/hello/')


def index(request):
    if request.user.is_authenticated:
        # print(request.user.id)
        user = User.objects.get(id=request.user.id)
        permission = user.profile.permission
        url = ''
        if permission == 1:
            url = '/stu_resource/'
        elif permission == 2:
            url = '/teacher_resource/'
        elif permission == 3:
            url = '/assistant_resource/'
        elif permission == 4:
            url = '/edu_admin_resource/'
        return HttpResponseRedirect(url)
    return render(request, "studentsystem/fox1.html")
    # return HttpResponseRedirect('/accounts/login/')


@login_required()
def stu_resource(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_resource.html')


@login_required()
def teacher_resource(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource.html')


@login_required()
def assistant_resource(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_resource.html')


@login_required()
def stu_pt(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_pt.html')


@login_required()
def stu_grade(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_grade.html')


@login_required()
def stu_chat(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_chat.html')


@login_required()
def stu_hw(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_hw.html')


@login_required()
def stu_panels(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_panels.html')


@login_required()
def stu_hw1(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_hw_1.html')


@login_required()
def stu_hw2(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_hw_2.html')


@login_required()
def teacher_resource_a(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource_a.html')


@login_required()
def teacher_resource_b(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource_b.html')


@login_required()
def teacher_chat_1(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_chat_1.html')


@login_required()
def teacher_chat(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_chat.html')


@login_required()
def teacher_grade(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_grade.html')


@login_required()
def teacher_hw_1(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_hw_1.html')


@login_required()
def teacher_hw(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_hw.html')


@login_required()
def teacher_hw_2(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_hw_2.html')


@login_required()
def teacher_panels(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_panels.html')


@login_required()
def teacher_resource_1_a(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource_1_a.html')


@login_required()
def teacher_resource_1_b(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource_1_b.html')


@login_required()
def teacher_resource_2_b(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_resource_2_b.html')


@login_required()
def teacher_stumanage(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_stumanage.html')


@login_required()
def teacher_stumanage_1(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_stumanage_1.html')


@login_required()
def teacher_stumanage_2_a(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_stumanage_2_a.html')


@login_required()
def teacher_stumanage_2_b(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_stumanage_2_b.html')


@login_required()
def assistant_chat(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_chat.html')


@login_required()
def assistant_chat_1(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_chat_1.html')


@login_required()
def assistant_hw(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_hw.html')


@login_required()
def assistant_hw_2(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_hw_2.html')


@login_required()
def assistant_hw_3(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_hw_3.html')


@login_required()
def assistant_hw_child1(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_hw_child1.html')


@login_required()
def assistant_panels(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_panels.html')


@login_required()
def assistant_pt(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_pt.html')


@login_required()
def assistant_resource(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_resource.html')


@login_required()
def assistant_resource2(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_resource2.html')


@login_required()
def assistant_resource_child1(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_resource_child1.html')


def charttest(request):
    return render(request, 'studentsystem/charttest.html')


@login_required()
def edu_admin_pt(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_pt.html')


@login_required()
def edu_admin_resource(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_resource.html')


@login_required()
def edu_admin_table(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_table.html')


@login_required()
def edu_admin_table1(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_table1.html')


@login_required()
def edu_admin_table_1(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_table_1.html')


def item(request):
    return render(request, 'studentsystem/item.html')


def mail(request):
    return render(request, 'studentsystem/mail.html')


@login_required()
def stu_chat_forhead(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_chat_forhead.html')


@login_required()
def teacher_chat_forhead(request):
    if request.user.profile.permission != 2:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/teacher_chat_forhead.html')


@login_required()
def assistant_chat_forhead(request):
    if request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/assistant_chat_forhead.html')


@login_required()
def edu_admin_table1_a(request):
    if request.user.profile.permission != 4:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/edu_admin_table1_a.html')


@login_required()
def stu_resource_1(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_resource_1.html')


@login_required()
def stu_chat_1(request):
    if request.user.profile.permission != 1 and request.user.profile.permission != 3:
        return HttpResponseRedirect('/')
    return render(request, 'studentsystem/stu_chat_1.html')


def changeaccount(request):
    return render(request, 'studentsystem/changeaccount.html')


def fox1(request):
    return render(request, 'studentsystem/fox1.html')


def fox2(request):
    return render(request, 'studentsystem/fox2.html')