# from django.shortcuts import render
from .models import Homework
from course.models import Courses
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from django.db.models import Max, Avg
from todolist.models import Todolist
# Create your views here.


def addHomework(request):
    if request.method == 'POST':
        myFile = request.FILES.get("filepath", None)

        course_id = request.POST.get('course')
        homework_name = request.POST.get('homework_name')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        user = request.user

        course_num = Homework.objects.filter(coid=course_id).filter(is_valid=1)
        num = len(course_num) + 1
        is_valid = 1
        grade = 0

        homework = Homework(coid=course_id, is_valid=is_valid, author=user,
                            homework_name=homework_name, content=content,
                            filepath=myFile, num=num, grade=grade, deadline=deadline)
        homework.save()

        # add the homework-todolist to every course_user
        course = Courses.objects.get(course_id=course_id)
        course_name = course.course_name
        list_content = course_name+homework_name
        list_time = deadline
        is_valid = 0

        students = []
        course_users = course.users.all()
        # profile = UserProfile.objects.filter(user_id__in=list(students)).values('permission')
        for course_user in course_users:
            permission = course_user.user.profile.permission
            if permission == 1 or permission == 3:
                students.append(course_user.user)

        for i in students:
            todolist = Todolist(content=list_content, list_time=list_time, is_valid=is_valid, author=i)
            todolist.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def submitHomework(request):
    if request.method == 'POST':
        myFile = request.FILES.get("filepath", None)

        course_id = request.POST.get('course')
        homework_name = request.POST.get('homework_name')
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        user = request.user

        course_num = Homework.objects.filter(coid=course_id).filter(is_valid=1)
        num = len(course_num) + 1
        is_valid = 0
        grade = 0

        homework = Homework(coid=course_id, is_valid=is_valid, author=user,
                            homework_name=homework_name, content=content,
                            filepath=myFile, num=num, grade=grade, deadline=deadline)
        homework.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


def getHomework(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')

        homeworks = Homework.objects.filter(coid=course_id).filter(is_valid=1)
        homework_list = []
        for i in homeworks:
            homework_list.append({'homework_id': i.homework_id,
                                  'homework_name': i.homework_name,
                                  'content': i.content,
                                  'filepath': i.filepath.path})

        res = {'num': len(homework_list),
               'homeworks': homework_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return


def checkHomework(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        homework_name = request.POST.get('homework_name')

        homeworks = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=0)
        homework_list = []
        for i in homeworks:
            homework_list.append({'homework_id': i.homework_id,
                                  'homework_name': i.homework_name,
                                  'content': i.content,
                                  'filepath': i.filepath.path})

        res = {'num': len(homework_list),
               'homeworks': homework_list,
               }

        return HttpResponse(json.dumps(res), content_type='application/json')
    return


def getoneHomework(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        homework_name = request.POST.get('homework_name')

        homework = Homework.objects.filter(coid=course_id).filter(homework_name=homework_name).filter(is_valid=1)
        path = homework.filepath.path

        return HttpResponse(json.dumps({'content': homework.content,
                                        'filepath': path,
                                        'deadline': homework.deadline}),
                            content_type='application/json')
    return


def correctHomework(request):
    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        grade = request.POST.get('grade')

        homework = Homework.objects.get(homework_id=homework_id)
        homework.grade = grade
        homework.save()

        return HttpResponse(json.dumps({'res': 'success'}), content_type='application/json')
    return


# 学生查看所有作业成绩
def getstudentGrade(request):
    if request.method == 'GET':
        user = request.user
        homeworks = Homework.objects.filter(author_id=user.id)

        grade_list = []
        for i in homeworks:
            course_id = i.course_id
            course = Courses.objects.get(course_id=course_id)
            course_name = course.course_name
            grade_list.append({'course_name': course_name,
                               'course_num': i.num,
                               'grade': i.grade})

        return HttpResponse(json.dumps(grade_list), content_type='application/json')
    return


# 老师查看所有学生的每次成绩
def getteacherGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        course = course_user.course

        grade_list = []
        # 老师教授的课程
        for i in course:
            course_name = i.course_name
            course_id = i.course_id
            homeworks = Homework.objects.filter(course_id=course_id).filter(is_valid=0)
            # 该课程下的每一次作业
            for j in homeworks:
                user_id = j.author_id
                homework_user = User.objects.get(id=user_id)
                name = homework_user.username
                grade_list.append({'course_name': course_name,
                                   'stu_name': name,
                                   'course_num': j.num,
                                   'grade': j.grade})

        return HttpResponse(json.dumps(grade_list), content_type='application/json')
    return


# 老师查看教授课程的最高分/平均分
def teacherGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        course = course_user.course

        best_grade_list = []
        average_grade_list = []
        for i in course:
            course_name = i.course_name
            course_id = i.course_id
            homeworks = Homework.objects.filter(course_id=course_id).filter(is_valid=0)

            best = homeworks.aggregate(Max('grade'))
            average = homeworks.aggregate(Avg('grade'))
            best_grade_list.append({'course_name': course_name,
                                    'grade': best})
            average_grade_list.append({'course_name': course_name,
                                       'grade': average})

        res = {'best': best_grade_list,
               'average': average_grade_list,
               }
        return HttpResponse(json.dumps(res), content_type='application/json')
    return


# 学生查看每门课程的最高分/平均分
def studentGrade(request):
    if request.method == 'GET':
        user = request.user
        course_user = user.course_user
        course = course_user.course

        best_grade_list = []
        average_grade_list = []
        for i in course:
            course_name = i.course_name
            course_id = i.course_id
            homeworks = Homework.objects.filter(course_id=course_id).filter(author_id=user.id)

            best = homeworks.aggregate(Max('grade'))
            average = homeworks.aggregate(Avg('grade'))
            best_grade_list.append({'course_name': course_name,
                                    'grade': best})
            average_grade_list.append({'course_name': course_name,
                                       'grade': average})

        res = {'best': best_grade_list,
               'average': average_grade_list,
               }
        return HttpResponse(json.dumps(res), content_type='application/json')
    return
