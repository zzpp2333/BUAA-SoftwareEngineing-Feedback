from django.shortcuts import render
from django.contrib.auth.models import User
import json
from django.http import HttpResponse, HttpResponseRedirect
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
    # return render(request, "studentsystem/login.html", {'msg': 'hello'})
    return HttpResponseRedirect('/accounts/login/')


def stu_resource(request):
    return render(request, 'studentsystem/stu_resource.html')


def teacher_resource(request):
    return render(request, 'studentsystem/teacher_resource.html')


def assistant_resource(request):
    return render(request, 'studentsystem/assistant_resource.html')


def stu_pt(request):
    return render(request, 'studentsystem/stu_pt.html')


def stu_grade(request):
    return render(request, 'studentsystem/stu_grade.html')


def stu_chat(request):
    return render(request, 'studentsystem/stu_chat.html')


def stu_hw(request):
    return render(request, 'studentsystem/stu_hw.html')


def stu_panels(request):
    return render(request, 'studentsystem/stu_panels.html')


def stu_hw1(request):
    return render(request, 'studentsystem/stu_hw_1.html')


def stu_hw2(request):
    return render(request, 'studentsystem/stu_hw_2.html')


def teacher_resource_a(request):
    return render(request, 'studentsystem/teacher_resource_a.html')


def teacher_resource_b(request):
    return render(request, 'studentsystem/teacher_resource_b.html')


def teacher_chat_1(request):
    return render(request, 'studentsystem/teacher_chat_1.html')


def teacher_chat(request):
    return render(request, 'studentsystem/teacher_chat.html')


def teacher_grade(request):
    return render(request, 'studentsystem/teacher_grade.html')


def teacher_hw_1(request):
    return render(request, 'studentsystem/teacher_hw_1.html')


def teacher_hw(request):
    return render(request, 'studentsystem/teacher_hw.html')


def teacher_hw_2(request):
    return render(request, 'studentsystem/teacher_hw_2.html')


def teacher_panels(request):
    return render(request, 'studentsystem/teacher_panels.html')


def teacher_resource_1_a(request):
    return render(request, 'studentsystem/teacher_resource_1_a.html')


def teacher_resource_1_b(request):
    return render(request, 'studentsystem/teacher_resource_1_b.html')


def teacher_resource_2_b(request):
    return render(request, 'studentsystem/teacher_resource_2_b.html')


def teacher_stumanage(request):
    return render(request, 'studentsystem/teacher_stumanage.html')


def teacher_stumanage_1(request):
    return render(request, 'studentsystem/teacher_stumanage_1.html')


def teacher_stumanage_2_a(request):
    return render(request, 'studentsystem/teacher_stumanage_2_a.html')


def teacher_stumanage_2_b(request):
    return render(request, 'studentsystem/teacher_stumanage_2_b.html')


def assistant_chat(request):
    return render(request, 'studentsystem/assistant_chat.html')


def assistant_chat_1(request):
    return render(request, 'studentsystem/assistant_chat_1.html')


def assistant_hw(request):
    return render(request, 'studentsystem/assistant_hw.html')


def assistant_hw_child1(request):
    return render(request, 'studentsystem/assistant_hw_child1.html')


def assistant_panels(request):
    return render(request, 'studentsystem/assistant_panels.html')


def assistant_pt(request):
    return render(request, 'studentsystem/assistant_pt.html')


def assistant_resource(request):
    return render(request, 'studentsystem/assistant_resource.html')


def assistant_resource2(request):
    return render(request, 'studentsystem/assistant_resource2.html')


def assistant_resource_child1(request):
    return render(request, 'studentsystem/assistant_resource_child1.html')


def charttest(request):
    return render(request, 'studentsystem/charttest.html')


def edu_admin_pt(request):
    return render(request, 'studentsystem/edu_admin_pt.html')


def edu_admin_resource(request):
    return render(request, 'studentsystem/edu_admin_resource.html')


def edu_admin_table(request):
    return render(request, 'studentsystem/edu_admin_table.html')


def edu_admin_table1(request):
    return render(request, 'studentsystem/edu_admin_table1.html')


def edu_admin_table_1(request):
    return render(request, 'studentsystem/edu_admin_table_1.html')


def item(request):
    return render(request, 'studentsystem/item.html')


def mail(request):
    return render(request, 'studentsystem/mail.html')


def stu_chat_forhead(request):
    return render(request, 'studentsystem/stu_chat_forhead.html')


def teacher_chat_forhead(request):
    return render(request, 'studentsystem/teacher_chat_forhead.html')


def assistant_chat_forhead(request):
    return render(request, 'studentsystem/assistant_chat_forhead.html')


def edu_admin_table1_a(request):
    return render(request, 'studentsystem/edu_admin_table1_a.html')


def stu_resource_1(request):
    return render(request, 'studentsystem/stu_resource_1.html')


def stu_chat_1(request):
    return render(request, 'studentsystem/stu_chat_1.html')